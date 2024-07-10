# Módulos necessários para o funcionamento do código
from flask import Flask, request, jsonify
from flask_cors import CORS
from concurrent.futures import ThreadPoolExecutor
from data_processing import data_processing as processing
from database_manager import db_commands as db
from algorithms.general_executer import general_executer as executer

# Configuração da API
app = Flask(__name__)
CORS(app)

# Inicialização para utilização de threading
thread = ThreadPoolExecutor(2)
executing = False

# Configuração do banco de dados
db.generate_db()

# Rota para recebimento dos dados
@app.route('/sendData', methods = ["POST"])
async def send_data():
    global thread
    global executing
    if executing == False:
        try:
            # Arquivo vindo do front-end
            file = request.files.get("data").stream

            # Restrições
            max_days = int(request.form.get("days"))
            max_reads = int(request.form.get("leituras"))
            algorithm = int(request.form.get("algorithm"))

            # Parâmetros dos algoritmos
            args = []
            match algorithm:
                case 1: # Ant Colony
                    get_ant_colony_args(args, False)
                case 2: # Pollination
                    get_pollination_args(args, False)
                case 3: # Ant Colony + 2-Opt
                    get_ant_colony_args(args, True)
                case 4: # Pollination + 2-Opt
                    get_pollination_args(args, True)

            # Dados de base para futura junção com a resposta do algoritmo em java, tratados e otimizados para esse fim
            clean_initial_data = processing.prepare_initial_data(file)
            file.seek(0)

            # Dados a serem enviados como input para o algoritmo em java, tratados e otimizados para esse fim
            algorithm_data = processing.prepare_algorithm_data(file, max_days, max_reads)
            file.close()
    
            # Guardando no banco de dados os dados da execução
            EXECUTING_STATUS = 1
            inserted_id = db.alter_data("INSERT INTO EXECUTIONS (algorithm, status, start_time, days_limit, reads_limit) VALUES (?, ?, datetime(), ?, ?);", (algorithm, EXECUTING_STATUS, max_days, max_reads))
            
            thread.submit(executer.run_algorithm, algorithm, algorithm_data, clean_initial_data, inserted_id, args)
            executing = True

            return "Executing algorithm.", 200 # HTML No Content
        
        except Exception as e:
            print(e)
            if "clean_initial_data" in locals() and not clean_initial_data.closed: clean_initial_data.close()
            if "algorithm_data" in locals() and not algorithm_data.closed: algorithm_data.close()
            if "file" in locals() and not file.closed: file.close()

            # Removendo os arquivos temporários criados
            processing.remove_generated_files()
            
            # Retornando erro ao front-end
            return e.__str__(), 400 # 400 = HTTP BAD REQUEST
    else:
        return "Task already in execution.", 200


# Rota para envio dos resultados
@app.route('/getResults', methods = ["GET"])
def get_results():
    global executing
    try:
        result = db.retrieve_data("SELECT id, status, result FROM EXECUTIONS WHERE id=(SELECT max(id) FROM EXECUTIONS);")
        if result == None or result == []:
            return '', 204 
        
        id = result[0][0]
        status = result[0][1]
        response = result[0][2]
        
        if not executing and status == 1:
            db.alter_data("DELETE * FROM EXECUTIONS WHERE id=?", (id,))
            return '', 204
        
        if status == 1: # Still executing
            return "Executing algorithm.", 200
        elif status == 2: # Finished execution
            executing = False
            return jsonify(response), 200 # 200 = HTTP SUCCESS
        else: # Error executing
            executing = False
            return "Error executing algorithm: " + response, 200
        
    except Exception as e:
        print(e)
        return "Error getting the results: " + e, 400


# Rota para envio dos algoritmos
@app.route('/getAlgorithms', methods = ["GET"])
def get_algorithms():
    try:
        result = db.retrieve_data("SELECT id, name FROM ALGORITHMS;")
        return jsonify({"algorithms" : [{result[i][1] : result[i][0]} for i in range(len(result))]}), 200
        
    except Exception as e:
        print(e)
        return "Error getting the algorithms: " + e, 400


# Preenche a lista "args" com os argumentos vindos do front-end acerca da execução do algoritmo Ant Colony com ou sem o 2-Opt
def get_ant_colony_args(args: list, two_opt : bool) -> None:
    args.append(int(request.form.get("antIterations")))
    args.append(int(request.form.get("alpha")))
    args.append(int(request.form.get("beta")))
    if two_opt:
        args.append(int(request.form.get("iterations")))


# Preenche a lista "args" com os argumentos vindos do front-end acerca da execução do algoritmo Pollination com ou sem o 2-Opt
def get_pollination_args(args: list, two_opt : bool) -> None:
    args.append(int(request.form.get("pollinationIterations")))
    args.append(float(request.form.get("probability")))
    args.append(float(request.form.get("radius")))
    if two_opt:
        args.append(int(request.form.get("iterations")))



if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)

