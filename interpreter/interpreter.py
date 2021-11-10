class Interpreter:

    def interp(self, tokens, env):
        while tokens:
            env = tokens.pop(0).apply(env)
        
        return env