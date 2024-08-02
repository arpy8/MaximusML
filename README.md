# MaximusML

Welcome to MaximusML! This application provides a seamless experience for users to upload datasets, train models using various machine learning algorithms, and store the models in AWS S3 for future use.

## Features

- **User Authentication**: Secure login and registration system to manage user access.
- **Dataset Upload**: Simple and intuitive interface for uploading datasets.
- **Model Training**: Automatically train models using five different algorithms:
  - Support Vector Machine (SVM)
  - Random Forest (RF)
  - AdaBoost (ADA)
  - Gradient Boosting Regressor (GBR)
  - Multi-Layer Perceptron (MLP)
  - Decision Tree (DT)
- **Download Models**: Download trained models from AWS S3 for easy deployment.

## Installation
   
### Prerequisites

- Python 3.10+
- AWS Account with S3 access
- Required Python packages (listed in `requirements.txt`)

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/arpy8/PreProd-Corp---Buildathon-2024---Gyatt-Maximus.git
   cd PreProd-Corp---Buildathon-2024---Gyatt-Maximus
   ```

2. **Install Dependencies**

   ```bash
   uv pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**

   Create a `.env` file in the root directory with the following variables:

   ```plaintext
   AWS_DEFAULT_REGION=your_aws_default_region
   AWS_ACCESS_KEY_ID=your_aws_access_key_id
   AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
   S3_BUCKET_NAME=your_s3_bucket_name
   ```

3. **Start the Application**

   ```bash
   streamlit run main.py
   ```

## Usage

1. **Register / Log In**

   Navigate to the registration or login page to create an account or log in.

2. **Upload Dataset**

   Once logged in, go to the upload page and upload your dataset (CSV/XLSX format).

3. **Train Models**

   After the dataset is uploaded, navigate to the model training page. Select the algorithms you want to use (SVM, RF, ADA, GBR, MLP, DT) and click "Train".

4. **Store Models**

   The trained models will automatically be stored in your configured AWS S3 bucket.

## Project Structure

```
├── static/               # Public files (Data, Models, etc.)
│   ├── data/             # Sample datasets
│   └── images/           # Images for the web interface
├── pycaret/              # Slightly tweaked version of pycaret
├── main.py               # Main application file
├── user_auth/            # User authentication and registration
├── utils.py              # Utility functions
├── train_model.py        # Model training and tuning
├── Dockerfile            # Docker file for deployment
├── requirements.txt      # List of required Python packages
└── sections.py           # Contains the three sections for the web interface
```

## Contributing

We welcome contributions! Please fork the repository and submit pull requests for any enhancements or bug fixes.

## License

This project is licensed under the MIT License.

## Team Members

- [@Arpit Sengar](https://github.com/arpy8)
- [@Lay Sheth](https://github.com/cloaky233)
- [@Rishav Raj Sinha](https://github.com/Rishav-Raj-Sinha)

## Contact

For any questions or suggestions, please contact [arpitsengar99@gmail.com].
