class GraphQLMutationError(Exception):
    def __init__(self, mutation_name: str, error: str):
        self.mutation_name = mutation_name
        self.error = error
        self.message = f"{mutation_name} mutation failed - {error}."
        super().__init__(self.message)
