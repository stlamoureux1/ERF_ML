# Building drop-in AI models for ERF

Goal: Build an ANN model that can function as a drop-in replacement for the Saturation Adjustment component
in ERF Microphysics.

Internship project from summer 2025. Read the draft write-up [here](https://github.com/stlamoureux1/CCI_Summer2025_Report/blob/development/Report/CCI_Summer2025_Report_Spencer_Lamoureux.pdf)

## Background

In summer 2025, interned at Lawrence Berkeley National Laboratory in the [Center for Computational Sciences and Engineering](https://ccse.lbl.gov). This repository contains the code for my final project, done in about four weeks, after my other tasks were done. Our goal was to examine the feasability of an AI surrogate for solving moisture-temperature balance equations at every time step of a large scale fluid dynamics simulation in the [ERF](https://github.com/erf-model/ERF) codebase. To do this I trained a multi-layer perceptron on synthetic data from a traditional Newton solver. The results were promising, but my main finding was that statistical error on static held-out samples does not guarantee success in a time-stepping simulation.

I also tried other architectures, including Kolmogorov-Arnold networks. I considered these because of nonlinearity of solutions to the Clausius-Clapeyron equations in the relevant regime. While converging rapidly with quite narrow layers, these were still costly to train and more specialized, so less suitable as a baseline.

## Reflections

Looking back now there are several things I would have done differently.
1. **Sampling:** Coming in with a better understanding of the thermodynamic principles in play would have helped me devise and evaluate sampling methods better. I was not able at that time to figure out whether our training data distribution was contributing to the instability inside our simulations.
2. **Systematize meta-parameter tuning:** The main meta-parameters I looked at were hidden-layer width, number of hidden layers, batch size, and learning rate, as initial passes pointed to these being the most influential on test error. This didn't leave time for thinking about optimizers and activation functions, for example. I also wound up repeating some work by not always tracking the testing systematically.
3. **Setting up the full simulation pipeline early:** ERF is a C++ codebase and we trained our model using PyTorch. This required some plumbing to embed our trained models. I worked first on minimizing test error as much as I could, and then set up the actual simulations, whereas it would have been better to start running the simulations early and iterating on those.

## Acknowledgements
Ann Almgren, Jean Sexton, Andy Nonaka, Aaron Lattanzi, and Bhargav Sudarshan from CCSE were all extremely welcoming, supportive, and generous with their time.
