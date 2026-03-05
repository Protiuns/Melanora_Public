def cortex_function(func):
    """Decorator que marca uma função como disponível para o córtex analítico."""
    func._cortex_function = True
    return func
