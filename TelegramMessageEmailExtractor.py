import re
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

# Dados de configuração fornecidos
API_ID = 000000
API_HASH = '' 
PHONE_NUMBER = '+5511' 

# Função para extrair e-mails de uma string de texto
def extract_emails(text):
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    return re.findall(email_pattern, text)

# Configuração do cliente Telegram
client = TelegramClient('session_name', API_ID, API_HASH)

async def main():
    print("Inicializando o cliente...")
    await client.connect()

    if not await client.is_user_authorized():
        try:
            await client.send_code_request(PHONE_NUMBER)
            code = input('Por favor, insira o código recebido: ')
            await client.sign_in(PHONE_NUMBER, code)
        except SessionPasswordNeededError:
            password = input('Por favor, insira sua senha: ')
            await client.sign_in(password=password)
    
    # ID ou nome de usuário da conversa/grupo
    chat_id = ''  # Substitua pelo ID do chat ou nome de usuário
    chat = await client.get_entity(chat_id)
    emails = []
    async for message in client.iter_messages(chat, limit=9000):  # Ajuste o limite conforme necessário
        if message.text:
            emails.extend(extract_emails(message.text))
    
    # Remover duplicatas
    emails = list(set(emails))

    # Salvar os e-mails em um arquivo
    with open('emailstraidos.txt', 'w') as file:
        for email in emails:
            file.write(email + '\n')
    
    print("Os e-mails extraídos foram salvos em 'emailstraidos.txt'.")

def run():
    with client:
        client.loop.run_until_complete(main())

if __name__ == "__main__":
    run()
