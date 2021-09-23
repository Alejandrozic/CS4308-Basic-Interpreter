"""
Tested with Python 3.6.4
"""

import interpreter.lexical_analyzer


file = 'source_files/example2.bas'
lexical_analyzer = interpreter.lexical_analyzer.LexicalAnalyzer(file)
lexical_analyzer.run()
