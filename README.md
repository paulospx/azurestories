# 🚀 Agile Story Creator 📝

A tool that utilizes Artificial Intelligence to generate Agile stories and sends them to an Azure Board.

## 🔍 Introduction

This project is a tool that uses Artificial Intelligence to create Agile stories and sends them to an Azure Board. The goal of this project is to automate the process of creating and sending stories for your team's backlog.

![Azure Stories](/images/landing.png)

Azure Stories

![Azure Stories Screenshot 1](/images/azure-stories-1.png)

![Azure Stories at Azure DevOps](/images/azure-stories-2.png)

## 🤔 Features

### 📝 AI-Powered Story Generation

- Uses LLM connection to Ollama to analyse user input and generate Agile stories.
- Supports multiple story formats, including Scrum and Kanban.

### 💻 Integration with Azure Boards

- Connects seamlessly to your Azure Board instance.
- Allows for easy import of generated stories into the board.

## 🚀 Installation

To install this project, follow these steps:

1. Clone this repository using `git clone https://github.com/paulospx/azurestories.git`
2. Install the required dependencies by running `pip install -r requirements.txt`
3. Set up your Azure Board credentials in the `config.py` file.

## 📝 Usage

To use this project, follow these steps:

1. Run the script using `streamlit run app.py`
2. Follow the prompts to input your team's story details.
3. The AI-powered story generator will create a story based on your input.
4. The generated story will be sent to your Azure Board instance.

## 🤝 Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork this repository using the GitHub fork button.
2. Create a new branch for your contribution: `git checkout -b feature/your-branch-name`
3. Make your changes and commit them using `git add .` and `git commit -m "Your message"`
4. Push your changes to your forked repository: `git push origin your-branch-name`

## 📝 License

This project is licensed under the MIT License. See [LICENSE](http://localhost:8501/LICENSE) for more information.

## 🚀 Requirements

- Python 3.8+
- Azure Board API credentials PAT
- Streamlit and Ollama

## 💻 Known Issues

- Occasional AI-powered story generation errors
