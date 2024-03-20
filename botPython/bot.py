from botcity.core import DesktopBot
from botcity.maestro import *

BotMaestroSDK.RAISE_NOT_CONNECTED = False

CAMINHO_FAKTURAMA = r"C:\Program Files\Fakturama2\Fakturama.exe"

def main():
    maestro = BotMaestroSDK.from_sys_args()
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    try:
        bot = DesktopBot()

        # abrindo o fakturama
        bot.execute(CAMINHO_FAKTURAMA)

        # abrindo o arquivo .json
        with open('produtos.json') as json_file:
            json_data = json.load(json_file)

        # definindo um nome para a lista de produtos que consta no arquivo payload.json
        produtos_para_cadastrar = json_data["load"]["products"]

        for produto in produtos_para_cadastrar:
            # criar novo produto no fakturama
            if not bot.find("botao_novo_produto", matching=0.97, waiting_time=10000):
                not_found("botao_novo_produto")
            bot.click()
            
            # inicia o cadastro pelo item_number
            if not bot.find("campo_item_number", matching=0.97, waiting_time=10000):
                not_found("campo_item_number")
            bot.click_relative(88, 9)
            bot.type_keys(produto["item_number"])
            
            # prossegue com o cadastro
            bot.tab()
            bot.type_keys(produto["name"])

            if not bot.find("campo_category", matching=0.97, waiting_time=10000):
                not_found("campo_category")
            bot.click_relative(62, 6)
            bot.type_keys(produto["category"])

            if not bot.find("campo_gtin", matching=0.97, waiting_time=10000):
                not_found("campo_gtin")
            bot.click_relative(69, 6)
            bot.type_keys(produto["gtin"])
            
            if not bot.find("campo_supplier_code", matching=0.97, waiting_time=10000):
                not_found("campo_supplier_code")
            bot.click_relative(96, 4)
            bot.type_keys(produto["supplier_code"])

            # em algumas situações, podemos usar o tab ou continuar mapeando pela visão computacional para trocar de campo
            bot.tab()
            bot.type_keys(produto["description"])

            if not bot.find("campo_price", matching=0.97, waiting_time=10000):
                not_found("campo_price")
            bot.click_relative(136, 4)
            bot.control_a()
            bot.type_keys(produto["price"])
            
            if not bot.find("campo_cost", matching=0.97, waiting_time=10000):
                not_found("campo_cost")
            bot.click_relative(114, 3)
            bot.control_a()
            bot.type_keys(produto["cost"])
            
            if not bot.find("campo_allowance", matching=0.97, waiting_time=10000):
                not_found("campo_allowance")
            bot.click_relative(67, 6)
            bot.type_keys(produto["allowance"])

            bot.tab()

            if not bot.find("campo_stock", matching=0.97, waiting_time=10000):
                not_found("campo_stock")
            bot.click_relative(60, 5)
            bot.control_a()
            bot.type_keys(produto["stock"])
            
            # precisamos salvar o produto
            if not bot.find("botao_save", matching=0.97, waiting_time=10000):
                not_found("botao_save")
            bot.click()

            # precisamos fechar a aba do produto que foi criado
            bot.control_w()       

            # criando um log de atividade
            maestro.new_log_entry(
                activity_label="cadastro_produtos",
                values = {
                    "produto": produto["name"],
                    "mensagem": "Cadastrado com sucesso.",
                    "status": "Sucesso"
                }
            )

            # criando um exemplo de alerta
            maestro.alert(
                task_id=execution.task_id,
                title="Alerta cadastro de produto",
                message=f"O cadastro do produto {produto['name']} foi realizado com sucesso.",
                alert_type=AlertType.INFO
            )

        # fecha o fakturama
        bot.alt_f4()

        # seta as informações nas variáveis para finalizar a tarefa
        status = AutomationTaskFinishStatus.SUCCESS
        message = "Execução concluída com sucesso."
    except:
        # seta as informações nas variáveis para finalizar a tarefa
        status = AutomationTaskFinishStatus.FAILED
        message = "Execução falhou."    
    finally:
        print("Finalizando a execução.")
        maestro.finish_task(
            task_id=execution.task_id,
            status=status,
            message=message
        )

# apenas outro exemplo de como abrir o fakturama: mapeando pela visão computacional
def abrir_fakturama(bot: DesktopBot):
    # busca a barra de pesquisa do windows
    if not bot.find("botao_pesquisar", matching=0.97, waiting_time=10000):
        not_found("botao_pesquisar")
    bot.click()
    
    # digita o nome do programa
    bot.type_keys("Fakturama.exe")
    bot.wait(1000)
    bot.enter()

def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()