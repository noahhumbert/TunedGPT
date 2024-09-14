from waitress import serve
import main  # or the name of your app's module

serve(main.app, host='0.0.0.0', port=5000)