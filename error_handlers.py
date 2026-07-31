from flask import jsonify


class TriagemError(Exception):
    def __init__(self, message, code=400):
        self.message = message
        self.code = code
        super().__init__(self.message)


class DadosInvalidosError(TriagemError):
    def __init__(self, message="Dados inválidos"):
        super().__init__(message, 400)


class PacienteNaoEncontradoError(TriagemError):
    def __init__(self, message="Paciente não encontrado"):
        super().__init__(message, 404)


class OllamaIndisponivelError(TriagemError):
    def __init__(self, message="Serviço de IA indisponível"):
        super().__init__(message, 503)


def registrar_handlers(app):
    @app.errorhandler(TriagemError)
    def handle_triagem_error(error):
        return jsonify({"erro": error.message}), error.code

    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({"erro": "Recurso não encontrado"}), 404

    @app.errorhandler(500)
    def handle_internal_error(error):
        return jsonify({"erro": "Erro interno do servidor"}), 500

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        return jsonify({"erro": "Método não permitido"}), 405
