import requests
import os
import shutil
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage

# ID fornecido
DOCTOR_ID = "af7aec4e-e0ba-43c3-9af1-55a9348d470f"
RELATORIOS_DIR = "C:\\Relatorios2"
FATURADOS_DIR = "C:\\Faturados"
LOG_DIR = "C:\\Logs"

# Função para verificar se os arquivos estão presentes na pasta Relatorios
def verificar_arquivos(arquivo):
    nome_base, _ = os.path.splitext(arquivo)
    pdf_path = os.path.join(RELATORIOS_DIR, f"{nome_base}.pdf")
    rbd_path = os.path.join(RELATORIOS_DIR, f"{nome_base}.rbd")
    return os.path.exists(pdf_path) and os.path.exists(rbd_path)

def enviar_arquivo_para_endpoint(arquivo, log_file):
    url = 'https://telemed.rwedev.com/api/report/store-external'
    nome_base, _ = os.path.splitext(arquivo)
    files = {
        'file': (f"{nome_base}.pdf", open(os.path.join(RELATORIOS_DIR, f"{nome_base}.pdf"), 'rb'), 'application/pdf'),
        'rbd': (f"{nome_base}.rbd", open(os.path.join(RELATORIOS_DIR, f"{nome_base}.rbd"), 'rb'), 'application/octet-stream')
    }

    data = {
        'doctor_id': DOCTOR_ID
    }

    response = requests.post(url, files=files, data=data)

    if response.status_code == 200:
        log_file.write(f"{datetime.now()} - Arquivos {nome_base}.pdf e {nome_base}.rbd enviados com sucesso para o endpoint.\n")
        return True
    else:
        log_file.write(f"{datetime.now()} - Erro ao enviar os arquivos {nome_base}.rbd e {nome_base}.pdf para o endpoint. Status: {response.status_code} - {response.text}\n")
        return False

def mover_arquivos_para_faturados(arquivo):
    origem_pdf = os.path.join(RELATORIOS_DIR, f"{arquivo}.pdf")
    origem_rbd = os.path.join(RELATORIOS_DIR, f"{arquivo}.rbd")
    destino_pdf = os.path.join(FATURADOS_DIR, f"{arquivo}.pdf")
    destino_rbd = os.path.join(FATURADOS_DIR, f"{arquivo}.rbd")
    try:
        shutil.move(origem_pdf, destino_pdf)
        shutil.move(origem_rbd, destino_rbd)
        print(f"Arquivos {arquivo}.pdf e {arquivo}.rbd movidos para {FATURADOS_DIR}.")
        return True
    except Exception as e:
        print(f"Erro ao mover os arquivos {arquivo}.pdf e {arquivo}.rbd para {FATURADOS_DIR}: {e}")
        return False

def main():
    print("Iniciando o script...")
    
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    # Criar diretório para os logs desta execução
    data_hora_execucao = datetime.now().strftime("%Y-%m-%d_%H-%M")
    dir_execucao = os.path.join(LOG_DIR, data_hora_execucao)
    os.makedirs(dir_execucao)

    log_file_path = os.path.join(dir_execucao, "log.txt")
    log_erro_path = os.path.join(dir_execucao, "log_erro.txt")

    with open(log_file_path, "a") as log_file, open(log_erro_path, "w") as log_erro_file:
        log_file.write(f"\n\n------ Novo Registro - {datetime.now()} ------\n")
        
        arquivos_relatorios = set(os.path.splitext(arquivo)[0] for arquivo in os.listdir(RELATORIOS_DIR))

        for arquivo_base in arquivos_relatorios:
            if verificar_arquivos(arquivo_base):
                if not enviar_arquivo_para_endpoint(arquivo_base, log_file):
                    print("Erro ao enviar arquivos para o endpoint.")
                    log_erro_file.write(f"{datetime.now()} - Erro ao enviar arquivos {arquivo_base}.pdf e {arquivo_base}.rbd para o endpoint.\n")
                    continue  

                if not mover_arquivos_para_faturados(arquivo_base):
                    print("Erro ao mover arquivos para a pasta Faturados.")
                    log_file.write(f"{datetime.now()} - Erro ao mover arquivos para a pasta Faturados.\n")
                else:
                    print(f"Arquivos {arquivo_base}.pdf e {arquivo_base}.rbd enviados com sucesso para o endpoint e movidos para {FATURADOS_DIR}.")
                    log_file.write(f"{datetime.now()} - Arquivos {arquivo_base}.pdf e {arquivo_base}.rbd enviados com sucesso para o endpoint e movidos para {FATURADOS_DIR}.\n")
            else:
                print(f"Arquivos correspondentes não encontrados para {arquivo_base}.")
                log_file.write(f"{datetime.now()} - Arquivos correspondentes não encontrados para {arquivo_base}.\n")

    # Se houver erros, envia o email com o anexo
    if os.path.getsize(log_erro_path) > 0:
        enviar_email_erro(log_erro_path, "Cardios03")

    input("Pressione Enter para buscar e enviar o arquivo amanhã...")

def enviar_email_erro(log_erro_path, maquina):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "ti@rwetelemedicina.com.br"
    receiver_email = "ti@rwetelemedicina.com.br"
    password = 'rwitvufzieyhflbj'

    message = EmailMessage()
    message["Subject"] = "Erro no envio de arquivos para o endpoint"
    message["From"] = sender_email
    message["To"] = receiver_email
    message.set_content(f"Erro no envio de arquivos para o endpoint.\n\nMaquina: {maquina}")

    with open(log_erro_path, "rb") as attachment:
        attachment_content = attachment.read()
        message.add_attachment(attachment_content, maintype="text", subtype="plain", filename=os.path.basename(log_erro_path))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.send_message(message)

if __name__ == "__main__":
    main()
