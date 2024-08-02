ML_MODELS = ["svm", "dt", "rf", "ada", "gbr", "mlp"]

MODEL_INFO = {
    "AdaBoostRegressor": "An AdaBoost regressor is a meta-estimator that begins by fitting a regressor on the original dataset and then fits additional copies of the regressor on the same dataset but where the weights of instances are adjusted according to the error of the current prediction. As such, subsequent regressors focus more on difficult cases.",
    "GradientBoostingRegressor": "This estimator builds an additive model in a forward stage-wise fashion; it allows for the optimization of arbitrary differentiable loss functions. In each stage a regression tree is fit on the negative gradient of the given loss function.",
    "DecisionTreeRegressor": "A decision tree is a flowchart-like structure where each internal node represents a feature or attribute and each branch represents a decision rule. The tree is grown by recursively partitioning the set of observations into subsets according to the values of the chosen features, stopping when some condition is met (e.g. reaching a certain depth in the tree or a node with a minimum number of observations).",
    "RandomForestRegressor": "A random forest is a meta estimator that fits a number of decision tree classifiers on various sub-samples of the dataset and uses averaging to improve the predictive accuracy and control over-fitting.",
    "SVR": "Support Vector Regression (SVR) is a linear model that can be used for both classification and regression. The goal of SVR is to find a hyperplane that best fits the data, and then predict the target variable based on the hyperplane.",
    "MLPRegressor": "A multilayer perceptron (MLP) is a feedforward artificial neural network with one or more hidden layers. It is a supervised learning algorithm that can be used for regression and classification tasks.",
}
