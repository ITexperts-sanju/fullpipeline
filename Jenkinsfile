stage('Unit Tests') {
    steps {
        echo "Running Python Unit Tests..."
        sh '''
        docker run --rm \
          -v $WORKSPACE:/app -w /app \
          python:3.11-slim bash -c "
            if [ -f requirements.txt ]; then
                pip install --no-cache-dir -r requirements.txt
            fi
            pip install --no-cache-dir pytest || true
            if [ -d tests ]; then
                pytest tests --maxfail=1 --disable-warnings -q || true
            else
                echo 'No tests directory found, skipping unit tests.'
            fi
          "
        '''
    }
}
