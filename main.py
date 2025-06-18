import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

# Asegúrate de tener los recursos de NLTK necesarios
try:
    nltk.data.find('tokenizers/punkt')
except nltk.downloader.DownloadError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except nltk.downloader.DownloadError:
    nltk.download('stopwords')

# 🔹 Nuevos Documentos sobre Civilizaciones Antiguas
documents = {
    "doc1": "Los egipcios construyeron las pirámides y desarrollaron una escritura jeroglífica.",
    "doc2": "La civilización romana fue una de las más influyentes en la historia occidental.",
    "doc3": "Los mayas eran expertos astrónomos y tenían un avanzado sistema de escritura.",
    "doc4": "La antigua Grecia sentó las bases de la democracia y la filosofía moderna.",
    "doc5": "Los sumerios inventaron la escritura cuneiforme y fundaron las primeras ciudades"
}

# 🔹 1. Función para tokenizar y limpiar documentos
def preprocess_document(text):
    """
    Tokeniza, convierte a minúsculas, elimina signos de puntuación y stopwords.
    """
    # Convertir a minúsculas
    text = text.lower()
    # Eliminar signos de puntuación (mantener solo letras y números)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    # Tokenizar
    tokens = word_tokenize(text)
    # Eliminar stopwords en español
    stop_words = set(stopwords.words('spanish'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    return filtered_tokens

# 🔹 2. Crear un índice invertido
def create_inverted_index(docs):
    """
    Crea un índice invertido a partir de un diccionario de documentos.
    Asocia cada palabra clave con el conjunto de IDs de documentos en los que aparece.
    """
    inverted_index = {}
    for doc_id, text in docs.items():
        processed_tokens = preprocess_document(text)
        for token in processed_tokens:
            if token not in inverted_index:
                inverted_index[token] = set()
            inverted_index[token].add(doc_id)
    return inverted_index

# 🔹 Funciones para operaciones booleanas
def boolean_and(set1, set2):
    return set1.intersection(set2)

def boolean_or(set1, set2):
    return set1.union(set2)

def boolean_not(set1, all_docs):
    return all_docs.difference(set1)

# 🔹 3. Procesar consulta booleana
def search_boolean_query(query, inverted_index, all_doc_ids):
    """
    Procesa una consulta booleana y devuelve los documentos relevantes.
    Soporta AND, OR, NOT.
    """
    query_parts = query.lower().split()
    
    if not query_parts:
        return set()

    # Manejar NOT al principio de la consulta
    if len(query_parts) == 2 and query_parts[0] == 'not':
        term = query_parts[1]
        if term in inverted_index:
            return boolean_not(inverted_index[term], all_doc_ids)
        else:
            return all_doc_ids # Si el término NOT no existe, todos los documentos son relevantes.

    # Consulta con dos términos y un operador
    if len(query_parts) == 3:
        term1, operator, term2 = query_parts
        set1 = inverted_index.get(term1, set())
        set2 = inverted_index.get(term2, set())

        if operator == 'and':
            return boolean_and(set1, set2)
        elif operator == 'or':
            return boolean_or(set1, set2)
        elif operator == 'not': # Este 'not' es para el caso 'term1 NOT term2'
            return boolean_not(set2, set1) # Documentos en set1 que NO están en set2
        else:
            return set() # Operador no reconocido
    
    # Consulta con un solo término
    if len(query_parts) == 1:
        term = query_parts[0]
        return inverted_index.get(term, set())

    return set() # Consulta no válida

# --- Ejecución principal del programa ---
if __name__ == "__main__":
    print("Iniciando la configuración del programa de búsqueda booleana...")
    
    # Crear el índice invertido
    inverted_index = create_inverted_index(documents)
    
    # Obtener todos los IDs de documentos para la operación NOT
    all_document_ids = set(documents.keys())

    print("\n¡Programa listo para realizar búsquedas booleanas!")
    print("Documentos disponibles:")
    for doc_id, text in documents.items():
        print(f"- {doc_id}: {text}")
    print("\nPuedes usar los operadores AND, OR, NOT.")
    print("Ejemplos: 'egipcios AND piramides', 'mayas OR escritura', 'grecia NOT moderna', 'romana'\n")

    while True:
        query = input("Ingrese una consulta booleana (o 'salir' para terminar): ").strip()
        if query.lower() == 'salir':
            print("Saliendo del programa. ¡Hasta luego!")
            break
        
        # Procesar y mostrar resultados
        results = search_boolean_query(query, inverted_index, all_document_ids)
        
        if results:
            print(f"📄 Documentos encontrados: {results}")
        else:
            print("❌ No se encontraron documentos para esta consulta.")
        print("-" * 30)