
import sys
import os
import importlib.util

from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config.environments import Environment
from helpers.log import Log

if __name__ == "__main__":

    load_dotenv()

    os.environ["ENVIRONMENT"] = Environment.TESTING.value

    if len(sys.argv) > 1:
        if sys.argv[1] == 'test_file':
            # Code to run when test_file parameter is provided
            if len(sys.argv) > 2 and sys.argv[2]:
                Log()(f'Running testfile: {sys.argv[2]}...')
            else:
                Log().error('No testfile path provided...')
        elif sys.argv[1] == 'test':
            # Code to run when test parameter is provided
            if len(sys.argv) > 2 and sys.argv[2]:
                Log()(f'Running specific test with name: {sys.argv[2]}...')
            else:
                Log().error('No testname provided...')
        else:
            # Default case if no valid parameter is provided
            Log()(f'Invalid parameter. Please use either:\n'
                        '- "python test.py test_file <testfile_path>" or\n'
                        '- "python test.py test <testname>"')
    else:
        # Default case if no parameter is provided
        Log()(f'Searching for testfiles...')

        files = []

        directory = os.path.dirname(__file__)
        for filename in os.listdir(directory):
            # Überprüfe, ob die Datei eine .py-Datei ist und nicht die aktuelle Datei
            if filename.endswith('.py') and filename != os.path.basename(__file__):
                file_path = os.path.join(directory, filename)
                files.append(file_path)

        Log()(f'Running all found tests...')

        for file in files:
            Log()(f"\n--- Führe Datei aus: {os.path.relpath(file, os.path.dirname(__file__))} ---")
            
            # Lade das Modul
            spec = importlib.util.spec_from_file_location("module.name", file)
            module = importlib.util.module_from_spec(spec)
            
            # Führe den Code aus
            spec.loader.exec_module(module)

            # Überprüfe, ob eine run-Funktion existiert
            if hasattr(module, 'run') and callable(module.run):
                results = module.run()  # Führe die run-Funktion aus
                
                if results[1] > 0:
                    Log().error(f"{results[1]} Tests fehlgeschlagen und {results[0]} Tests erfolgreich ausgeführt in {os.path.basename(file)}")
                else:
                    Log().success(f"{results[0]} Tests erfolgreich ausgeführt in {os.path.basename(file)}")
            else:
                Log().error(f"Keine run()-Funktion in {os.path.relpath(file, os.path.dirname(__file__))} gefunden.")
        
