import argparse

import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import joblib

import matplotlib.pyplot as plt

from torch.utils.data import TensorDataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

from tqdm import tqdm

#
# I/O
#

parser = argparse.ArgumentParser()
parser.add_argument("-w", "--width", help="Width of hidden layers. Default is 64", default=64)
parser.add_argument("-i", "--input-file", help="File name of sample input data for training. This file will get split into train/test/validation sets.")
parser.add_argument("-o", "--output-file", help="File name for parameters file resulting from training in .pt format.")
parser.add_argument("-e", "--epochs", help="Number of training epochs", default=1000)
parser.add_argument("-t", "--test-size", help="Ratio of data to hold out for testing, 0 < test_size < 1. Default is 0.3", default=0.3)
parser.add_argument("-s", "--early-stopping", help="If improvement on validation set is below this threshold on successive epochs, stop training to prevent over-fitting.", default=1e-6)
parser.add_argument("-p", "--plot-training", help="Display matplotlib scatter plot of training and validation error over training run. Uses a log-scale for y-axis.", action=argparse.BooleanOptionalAction)
parser.add_argument("-lr", "--learning-rate", help="Set learning rate used by Adam optimizer", default=1e-3)
parser.add_argument("-b", "--batch-size", help="Set batch size for minibatch training.", default=64)

args = parser.parse_args()

# Variables specified at command line
width = int(args.width)
input_file = args.input_file
output_file = args.output_file
epochs = int(args.epochs)
test_size = args.test_size
early_stopping = args.early_stopping
plot_training = args.plot_training
learning_rate = float(args.learning_rate)
batch_size = int(args.batch_size)

#
# Model: Multilayer Perceptron
#

class MLP(nn.Module):
    """
    Multi-layer perceptron with 2 hidden layers. Default width of hidden layers is 64 units.
    """
    def __init__(self, n_in, width, n_out):
        super(MLP, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(n_in, width),
            nn.ReLU(),
            nn.Linear(width, width),
            nn.ReLU(),
            nn.Linear(width, n_out)
        )

    def forward(self, x):
        return self.model(x)


#
# Read in data and perform conversions
#

df = pd.read_csv(input_file)

X = df[['T_in', 'qv_in', 'qc_in', 'pres_in']].values
Y = df[['T_out', 'qv_out', 'qc_out']].values

# Train/test split
# X_temp_arr, X_test_arr, Y_temp_arr, Y_test_arr = train_test_split(X, Y, test_size=test_size)

# rescale test-size for validation hold out
# val_size = test_size / (1 - test_size)
# X_train_arr, X_val_arr, Y_train_arr, Y_val_arr = train_test_split(X_temp_arr, Y_temp_arr, test_size=val_size)

#
# Variable scaling
#

# log transform pressure (input only), since it ranges over 3 orders of magnitude
X[:,3] = np.log10(X[:,3])

X[:,1] = np.log1p(X[:,1])
Y[:,1] = np.log1p(Y[:,1])

# log scale qc_in, accounting for value 0
X[:,2] = np.log1p(X[:,2])
Y[:,2] = np.log1p(Y[:,2])

# Train/test split
X_temp_arr, X_test_arr, Y_temp_arr, Y_test_arr = train_test_split(X, Y, test_size=test_size)

# rescale test-size for validation hold out
val_size = test_size / (1 - test_size)
X_train_arr, X_val_arr, Y_train_arr, Y_val_arr = train_test_split(X_temp_arr, Y_temp_arr, test_size=val_size)

# Use linear scaling for all variables.
scaler_X = MinMaxScaler()
scaler_Y = MinMaxScaler()

# Fit scaling transform to training data.
scaler_X.fit(X_train_arr)
scaler_Y.fit(Y_train_arr)

# pickle scalers to use on separate data
# joblib.dump(scaler_X, 'scaler_X.pkl')
# joblib.dump(scaler_Y, 'scaler_Y.pkl')

# Apply MinMax transform and convert to torch tensors
X_train = torch.from_numpy(scaler_X.transform(X_train_arr))
X_val = torch.from_numpy(scaler_X.transform(X_val_arr))
X_test = torch.from_numpy(scaler_X.transform(X_test_arr))

Y_train = torch.from_numpy(scaler_Y.transform(Y_train_arr))
Y_val = torch.from_numpy(scaler_Y.transform(Y_val_arr))
Y_test = torch.from_numpy(scaler_Y.transform(Y_test_arr))

# Set up data loader for minibatch training
dataset_train = TensorDataset(X_train, Y_train)
dataloader_train = DataLoader(dataset_train, batch_size=batch_size, shuffle=True)

#
# Setup and train model
#

# input sizes are fixed
n_in = 4
n_out = 3

# Instantiate MLP. Use float64.
net = MLP(n_in, width, n_out)
net.double()

# training properties
m_tol = 1e-6
criterion = nn.MSELoss()
# when I actually plotted training loss, there was heavy oscillation in later epochs
# a smaller learning rate seems to alleviate this
optimizer = optim.Adam(net.parameters(), lr=learning_rate)

# save training loss to plot later
train_loss_history = []
val_loss_history = []

epoch_count = 0

# Model training
for epoch in tqdm(range(epochs)):
    epoch_count += 1

    # training steps proper
    net.train()
    epoch_train_loss = 0
    num_train_samples = 0
    for X_batch, Y_batch in dataloader_train:
        optimizer.zero_grad()
        Y_pred_batch = net(X_batch)
        batch_loss = criterion(Y_pred_batch, Y_batch)
        batch_loss.backward()
        optimizer.step()

        epoch_train_loss += batch_loss.item() * X_batch.size(0)
        num_train_samples += X_batch.size(0)

    avg_epoch_train_loss = epoch_train_loss / num_train_samples
    train_loss_history.append(avg_epoch_train_loss)

    if epoch % 500 == 0:
        print(f"Epoch {epoch}, Loss: {avg_epoch_train_loss:.3e}")

    if epoch == epochs - 1:
        print(f"Final training loss after {epochs} epochs: {avg_epoch_train_loss:.3e}")

    # validation steps
    net.eval()
    Y_pred_val = net(X_val)
    val_loss = criterion(Y_pred_val, Y_val)
    val_loss_history.append(val_loss.item())

    if (val_loss < m_tol) :
        print(f"Breaking at Epoch {epoch}, Validation Loss: {val_loss.item():.3e}")
        break

    if epoch % 500 == 0:
        print(f"Validation loss: {val_loss.item():.3e}")



if plot_training:
    plt.scatter(range(epoch_count), train_loss_history, marker='.', alpha=0.2, label='training loss (MSE)')
    plt.scatter(range(epoch_count), val_loss_history, marker='.', alpha=0.2, color='red', label='validation loss (MSE)')
    plt.yscale('log')


# testing
net.eval()
with torch.no_grad():
    Y_pred = net(X_test)
    loss = criterion(Y_pred, Y_test)

    print(f"Test MSE: {loss.item():.3e}")

    plt.scatter(epoch_count, loss.item(), color='green', label='test loss (MSE)')
    plt.legend()
    plt.show()

# model export
scripted_model = torch.jit.script(net)
scripted_model.save(output_file)


