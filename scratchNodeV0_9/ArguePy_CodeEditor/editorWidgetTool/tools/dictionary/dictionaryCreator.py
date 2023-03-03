# Apriamo il file di testo in lettura
import string

operators = [
    '=',
    # Comparison
    '==', '!=', '<', '<=', '>', '>=',
    # Arithmetic
    '\+', '-', '\*', '/', '//', '\%', '\*\*',
    # In-place
    '\+=', '-=', '\*=', '/=', '\%=',
    # Bitwise
    '\^', '\|', '\&', '\~', '>>', '<<',
]


class dictionaryCreator:
    alphabetList = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                    'U', 'V', 'W', 'X', 'Y', 'Z']

    itaDictionary = r"/home/tedk/Desktop/python/pythonCodeEditor/editorWidgetTool/tools/dictionary/itaDictionary.py"
    engDictionary = r"/home/tedk/Desktop/python/pythonCodeEditor/editorWidgetTool/tools/dictionary/engDictionary.py"

    def createDictionary(self, inputFileName, outputFileName):
        """
        crea un file python con un dizionario contenente le parole di inputFileName
        le parole sono divise per lettera e incluse in una lista in modo che non siano più di 500 parole per lista
        il dizionario è scritto in questo modo:
        [A] _ [500word] = ['A', 'A-horizon', 'A-ok', 'Aa', 'Aaa', 'Aachen'..... ]
        e contine le parole che iniziano con la lettera [A] contanto 500 parole per lista le la 500esima parola è [500word]
        :param inputFileName:
        :param outputFileName:
        :return:
        """
        with open(inputFileName, 'r') as f:
            # Inizializziamo un dizionario vuoto
            allWords = f.read()
            # separa le parole in base alla lettera iniziale
            dict_liste = {}
            for letter in self.alphabetList:
                dict_liste[letter] = []
                for word in allWords.split():
                    if word[0] == letter.lower():
                        dict_liste[letter].append(word)

        wordList = ""
        print(len(dict_liste["A"]))

    def test(self):
        wordList = {c: [] for c in string.ascii_lowercase}
        with open("/home/tedk/Desktop/python/pythonCodeEditor/editorWidgetTool/tools/dictionary/wordListRaw/englishWords",
                  'r') as f:
            for line in f:
                word = line.strip()
                if word not in wordList:
                    try:
                        wordList[word[0]].append(word)
                    except:
                        pass

        with open("pyDictionary.py", 'w+') as f:
            f.write("wordList = {")
            for key, value in wordList.items():
                f.write(f"'{key}': {value},\n\n")
            f.write("}")

    @staticmethod
    def createDictionaryFromZero(inputFileName, outputFileName):
        import string

        with open(inputFileName, 'r') as f:
            # Inizializziamo un dizionario vuoto
            dict_liste = {}

            # Leggiamo il file di testo riga per riga
            for line in f:
                # Rimuoviamo eventuali spazi bianchi all'inizio o alla fine della riga
                word = line.strip()

                # Prendiamo il primo carattere della parola
                first_char = word[0]

                # Se la chiave non esiste nel dizionario, la creiamo e inizializziamo la lista vuota
                if first_char not in dict_liste:
                    dict_liste[first_char] = []

                # Aggiungiamo la parola alla lista corrispondente
                dict_liste[first_char].append(word)

        wordList = ""
        # Stampiamo le liste
        for key, value in dict_liste.items():
            wordList += f"{key}= {value} \n"

        with open(outputFileName, 'w') as f:
            f.write(wordList)

    @staticmethod
    def updateDictionary(existingDictionaryFileName, fileWithTheListOfWord, outputFileName):
        """
        existingDictionaryFileName: file contenente il dizionario esistente scritto in questo modo:
        A= ['A', 'A-horizon', 'A-ok', 'Aa', 'Aaa', 'Aachen'..... ]
        B= ['B', 'B-horizon', 'B-ok', 'Ba', 'Baa', 'Baal'..... ]
        Quello che fa la routine è aggiungere le parole mancanti al dizionario esistente cercandole
        nel file fileWithTheListOfWord e poi salvare il dizionario aggiornato in outputFileName
        :param existingDictionaryFileName: file esistente con il dizionario
        :param fileWithTheListOfWord: file con una lista di parole
        :param outputFileName:
        :return:
        """
        with open(existingDictionaryFileName, 'r') as f:
            # Inizializziamo un dizionario vuoto
            dict_liste = {}

            # Leggiamo il file di testo riga per riga
            for line in f:
                # Rimuoviamo eventuali spazi bianchi all'inizio o alla fine della riga
                word = line.strip()

                # Prendiamo il primo carattere della parola
                first_char = word[0]

                # Se la chiave non esiste nel dizionario, la creiamo e inizializziamo la lista vuota
                if first_char not in dict_liste:
                    dict_liste[first_char] = []

                # Aggiungiamo la parola alla lista corrispondente
                dict_liste[first_char].append(word)

        with open(fileWithTheListOfWord, 'r') as f:
            # Leggiamo il file di testo riga per riga
            for line in f:
                # Rimuoviamo eventuali spazi bianchi all'inizio o alla fine della riga
                word = line.strip()

                # Prendiamo il primo carattere della parola
                first_char = word[0]

                # Se la chiave non esiste nel dizionario, la creiamo e inizializziamo la lista vuota
                if first_char not in dict_liste:
                    dict_liste[first_char] = []

                # Aggiungiamo la parola alla lista corrispondente
                if word not in dict_liste[first_char]:
                    dict_liste[first_char].append(word)

        wordList = ""
        # Stampiamo le liste
        for key, value in dict_liste.items():
            wordList += f"{key}= {value} \n"

        with open(outputFileName, 'w') as f:
            f.write(wordList)

    def isNameInDictionary(self, word, dictionaryType):
        dictionaryFileName = None
        if dictionaryType == "eng":
            dictionaryFileName = "/home/tedk/Desktop/python/pythonCodeEditor/editorWidgetTool/tools/dictionary/englishWordList.py"
        elif dictionaryType == "ita":
            dictionaryFileName = "/home/tedk/Desktop/python/pythonCodeEditor/editorWidgetTool/tools/dictionary/italianWordList.txt"
        elif dictionaryType == "py":
            dictionaryFileName = "/home/tedk/Desktop/python/pythonCodeEditor/editorWidgetTool/tools/dictionary/pythonWordList.txt"

        if not dictionaryFileName:
            return None
        with open(dictionaryFileName, 'r') as f:
            if dictionaryType is ["eng", "ita"]:
                for line in f:
                    # Rimuoviamo eventuali spazi bianchi all'inizio o alla fine della riga
                    line = line.strip()
                    return self.searchWordByChar(line[0], word, line)
            elif dictionaryType == "py":
                if word in operators:
                    return True
                for line in f:
                    # Rimuoviamo eventuali spazi bianchi all'inizio o alla fine della riga
                    line = line.strip()

                    # Prendiamo il primo carattere della parola
                    first_char = line[0]
                    return self.searchWordByChar(first_char, word, line)
        return False

    def searchWordByChar(self, char, word, line):
        print(f"char: {char} word: {word} line: {line}")
        if char == word[0]:
            if word in line:
                return True
        return False


if __name__ == '__main__':
    dictionaryCreator = dictionaryCreator()
    aaa = dictionaryCreator.test()
