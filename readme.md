# Face Recognition Bot for Social and Law Enforcement Services

This project demonstrates a Telegram bot designed for facial recognition purposes. The bot enables users to process images, recognize faces, and manage a secure database of individuals for social and law enforcement applications. Built as an educational initiative within the FAI curriculum, it showcases modern AI technologies, development best practices, and ethical considerations.

---

## Project Goals and Objectives

### Goals:
- **Educational Value**: Provide a practical implementation of AI and machine learning concepts for face recognition.
- **Demonstrate Technologies**: Showcase the integration of neural networks, database management, and secure development practices.
- **Address Real-World Problems**: Support use cases like assisting vulnerable populations and identifying individuals in emergencies.

### Objectives:
1. Develop a Telegram bot capable of recognizing faces from images.
2. Use ArcFace, a state-of-the-art neural network, for generating high-dimensional facial embeddings.
3. Implement secure, scalable database operations for face data storage and retrieval.
4. Ensure the project aligns with ethical standards, including user privacy and data protection.

---

## Technologies Used

1. **Programming Languages**: Python.
2. **Machine Learning**: ArcFace for facial embedding.
3. **Database**:
   - SQLite for local data storage.
   - SQLAlchemy for ORM.
4. **Telegram Integration**: Using `python-telegram-bot` library.
5. **Docker**:
   - Docker images for deployment.
   - Docker Compose for managing multi-container environments.
6. **Libraries and Tools**:
   - `opencv-python` for image processing.
   - `insightface` for facial analysis.
   - `torch` and `onnxruntime` for neural network operations.

---

## Features

- **Facial Recognition**: Identifies individuals using cosine similarity of facial embeddings.
- **Image Handling**: Processes photos, detects faces, and extracts embeddings.
- **Database Operations**: Allows adding, updating, and querying face data securely.
- **Ethical Safeguards**:
   - Restricted access to the bot.
   - Logs for accountability.
   - Data removal upon user request.
- **User Interaction**: Guided data input with Telegram bot commands.

---

## Installation and Deployment

### Prerequisites
- Docker installed on your system.
  - For desktops: [Docker Desktop](https://www.docker.com/products/docker-desktop).
  - For servers (Ubuntu):
    ```bash
    sudo apt update
    sudo apt install apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    sudo apt update
    sudo apt install docker-ce
    sudo systemctl status docker
    sudo usermod -aG docker $USER
    ```

### Build Docker Image
1. Clone the repository and navigate to the project folder:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```
2. Build the Docker image:
   ```bash
   docker build -t face_recognition_bot .
   ```
3. Verify the image:
   ```bash
   docker images
   ```

### Run the Docker Container
1. Start the bot:
   ```bash
   docker run -d face_recognition_bot
   ```
2. Check running containers:
   ```bash
   docker ps
   ```

---

## Deployment to Server
1. Tag the Docker image:
   ```bash
   docker tag face_recognition_bot username/face_recognition_bot:latest
   ```
2. Push the image to Docker Hub:
   ```bash
   docker login
   docker push username/face_recognition_bot:latest
   ```
3. Pull the image on the server:
   ```bash
   docker pull username/face_recognition_bot:latest
   ```

### Using Docker Compose
Create a `docker-compose.yml` file:
```yaml
version: '3.8'

services:
  face_recognition_bot:
    image: username/face_recognition_bot:latest
    container_name: face_recognition_bot
    volumes:
      - ./resources:/app/resources
      - ./token.txt:/app/token.txt
    restart: unless-stopped
```
Deploy:
```bash
sudo docker compose up -d
```

---

## Future Enhancements
- **Scalability**: Adding support for Kubernetes deployments.
- **Improved Search**: Implementing Locality-Sensitive Hashing for faster database queries.
- **Advanced Features**: Multi-face recognition and support for larger datasets.
- **Enhanced Security**: Integrating TLS for secure communication.

---

## Ethical Considerations
- Respect user privacy by restricting access and encrypting data.
- Ensure transparency by logging all actions.
- Provide users with the ability to manage their data.

---

## References
1. Guo, Y., Zhang, L., Hu, Y., He, X., & Gao, J. (2020). ArcFace: Additive Angular Margin Loss for Deep Face Recognition. IEEE Transactions on Pattern Analysis and Machine Intelligence, 42(5), 1428-1442.
2. Luckin, R., Holmes, W., Griffiths, M., & Forcier, L. B. (2016). Intelligence Unleashed: An Argument for AI in Education. Pearson Education.

---

For questions or issues, please contact [@Alex_Grii](https://t.me/Alex_Grii).

