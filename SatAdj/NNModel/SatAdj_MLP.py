import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

#
# Model: Multilayer Perceptron
#

class MLP(nn.Module):
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

df = pd.read_csv('samples10k.csv')

X = df[['T_in', 'qv_in', 'qc_in', 'pres_in']].values
Y = df[['T_out', 'qv_out', 'qc_out']].values

# log transform pressure (input only)
X[:, 3] = np.log10(X[:, 3])

# Linear scaling for all variabls
scaler_X = MinMaxScaler()
scaler_Y = MinMaxScaler()

X = scaler_X.fit_transform(X)
Y = scaler_Y.fit_transform(Y)

# Validation split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.4)

# Convert to torch tensors, float64 by default
X_train = torch.from_numpy(X_train)
X_test = torch.from_numpy(X_test)
Y_train = torch.from_numpy(Y_train)
Y_test = torch.from_numpy(Y_test)

#
# Setup and train model
#

# input sizes are fixed
n_in = 4
n_out = 3

# width is a hyperparameter
width = 64

# instantiate MLP
net = MLP(n_in, width, n_out)
net.double()

# training properties
m_tol = 1e-6
criterion = nn.MSELoss()
optimizer = optim.Adam(net.parameters(), lr=0.001)

# training run
epochs = 5000
for epoch in range(epochs):
    net.train()

    Y_pred = net(X_train)
    loss = criterion(Y_pred, Y_train)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if (loss.item() < m_tol) :
        print(f"Breaking at Epoch {epoch}, Loss: {loss.item():.3e}")
        break

    if epoch % 500 == 0:
        print(f"Epoch {epoch}, Loss: {loss.item():.3e}")
        continue

    if epoch == epochs - 1:
        print(f"Final training loss after {epochs} epochs: {loss.item():.3e}")

# validation
net.eval()
with torch.no_grad():
    Y_pred = net(X_test)
    loss = criterion(Y_pred, Y_test)

    print(f"Test MSE: {loss.item():.3e}")

# model export
scripted_model = torch.jit.script(net)
scripted_model.save("SatAdj_MLP.pt")
















