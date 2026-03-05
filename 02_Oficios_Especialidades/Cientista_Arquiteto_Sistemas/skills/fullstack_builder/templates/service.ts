import { db } from '../config/database'; // Exemplo de import

export class TemplateService {
    /**
     * Busca todos os registros
     */
    static async getAll() {
        try {
            // return await db.model.findMany();
            return { message: "Not implemented yet" };
        } catch (error) {
            throw new Error(`Erro ao buscar dados: ${error.message}`);
        }
    }

    /**
     * Cria um novo registro
     */
    static async create(data: any) {
        // Validação Zod aqui
        return { id: 1, ...data };
    }
}
