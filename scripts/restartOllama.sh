ollama serve &
pid=$!

while ! pgrep -f "ollama"; do
  sleep 0.1
done

ollama list

echo Ollama is ready.