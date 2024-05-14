import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt  # Import matplotlib

# Function to calculate the correlation coefficients
def calculate_correlations(sum_x1, sum_x2, sum_x3, sum_x1x2, sum_x1x3, sum_x2x3, sum_x1_sq, sum_x2_sq, sum_x3_sq, n):
    # Calculate means
    mean_x1 = sum_x1 / n if sum_x1 else 0
    mean_x2 = sum_x2 / n if sum_x2 else 0
    mean_x3 = sum_x3 / n if sum_x3 else 0
    
    # Calculate variances
    var_x1 = (sum_x1_sq / n) - (mean_x1**2) if sum_x1_sq else 0
    var_x2 = (sum_x2_sq / n) - (mean_x2**2) if sum_x2_sq else 0
    var_x3 = (sum_x3_sq / n) - (mean_x3**2) if sum_x3_sq else 0
    
    # Calculate covariances
    cov_x1x2 = (sum_x1x2 / n) - (mean_x1 * mean_x2) if sum_x1x2 else 0
    cov_x1x3 = (sum_x1x3 / n) - (mean_x1 * mean_x3) if sum_x1x3 else 0
    cov_x2x3 = (sum_x2x3 / n) - (mean_x2 * mean_x3) if sum_x2x3 else 0
    
    # Calculate correlation coefficients
    r12 = cov_x1x2 / np.sqrt(var_x1 * var_x2) if var_x1 and var_x2 else 0
    r13 = cov_x1x3 / np.sqrt(var_x1 * var_x3) if var_x1 and var_x3 else 0
    r23 = cov_x2x3 / np.sqrt(var_x2 * var_x3) if var_x2 and var_x3 else 0
    
    # Partial correlation coefficient r31.2
    r31_2 = (r13 - r12 * r23) / np.sqrt((1 - r12**2) * (1 - r23**2)) if var_x1 and var_x2 and var_x3 else 0
    
    # Multiple correlation coefficient R1.23
    R1_23 = np.sqrt(r12**2 + r13**2 - 2 * r12 * r13 * r23) if var_x1 and var_x2 and var_x3 else 0
    
    return r31_2, R1_23

# Streamlit app
st.title("Correlation Coefficient Calculator")

st.write("This application calculates the partial correlation coefficient $r_{31.2}$ and the multiple correlation coefficient $R_{1.23}$ based on your input data.")

st.write("### Input Data")

# Let the user choose how to input data
input_type = st.selectbox("Choose how to input data", ("Enter raw data (X1, X2, X3)", "Enter summation values"))

if input_type == "Enter raw data (X1, X2, X3)":
    # Input fields for the raw data
    data_input = st.text_area("Enter the data for variables X1, X2, X3 as comma-separated values (each row on a new line):")
    if st.button("Calculate"):
        try:
            # Convert the input data to a DataFrame
            data = []
            for line in data_input.split("\n"):
                if line.strip():
                    data.append(list(map(float, line.split(","))))
            
            data = pd.DataFrame(data, columns=["X1", "X2", "X3"])

            # Calculate the correlations and get the correlation matrix
            r31_2, R1_23 = calculate_correlations(sum_x1, sum_x2, sum_x3, sum_x1x2, sum_x1x3, sum_x2x3, sum_x1_sq, sum_x2_sq, sum_x3_sq, n)

            # Display the raw data
            st.write("### Raw Data")
            st.write(data)

            # Plotting the correlation matrix
            plt.figure(figsize=(10, 8))
            plt.imshow(corr_matrix, cmap='coolwarm', interpolation='nearest')
            plt.colorbar(label='Correlation Coefficient')
            plt.title('Correlation Matrix')
            st.pyplot(plt)  # Display the plot in Streamlit

            # Scatter plot of X1 vs X2 and X1 vs X3
            plt.figure(figsize=(12, 6))
            plt.subplot(1, 2, 1)
            plt.scatter(data['X1'], data['X2'])
            plt.title('X1 vs X2')
            plt.xlabel('X1')
            plt.ylabel('X2')
            
            plt.subplot(1, 2, 2)
            plt.scatter(data['X1'], data['X3'])
            plt.title('X1 vs X3')
            plt.xlabel('X1')
            plt.ylabel('X3')
            
            st.pyplot(plt)  # Display the scatter plots in Streamlit

            # Display the results
            st.write("### Results")
            st.write(f"Partial correlation coefficient $r_{{31.2}}$: ${r31_2:.3f}$")
            st.write(f"Multiple correlation coefficient $R_{{1.23}}$: ${R1_23:.3f}$")

        except Exception as e:
            st.error(f"Error: {e}")
            st.write("Please ensure the data is in the correct format.")

elif input_type == "Enter summation values":
    # Input fields for the summation values
    sum_x1 = st.number_input("$\sum X_1$", value=0.0)
    sum_x2 = st.number_input("$\sum X_2$", value=0.0)
    sum_x3 = st.number_input("$\sum X_3$", value=0.0)
    sum_x1x2 = st.number_input("$\sum X_1X_2$", value=0.0)
    sum_x1x3 = st.number_input("$\sum X_1X_3$", value=0.0)
    sum_x2x3 = st.number_input("$\sum X_2X_3$", value=0.0)
    sum_x1_sq = st.number_input("$\sum X_1^2$", value=0.0)
    sum_x2_sq = st.number_input("$\sum X_2^2$", value=0.0)
    sum_x3_sq = st.number_input("$\sum X_3^2$", value=0.0)
    n = st.number_input("Number of observations", value=1, min_value=1)

    if st.button("Calculate"):
        try:
            # Calculate the correlations using summation values
            r31_2, R1_23 = calculate_correlations(sum_x1, sum_x2, sum_x3, sum_x1x2, sum_x1x3, sum_x2x3, sum_x1_sq, sum_x2_sq, sum_x3_sq, n)

            # Display the results
            st.write("### Results")
            st.write(f"Partial correlation coefficient $r_{{31.2}}$: ${r31_2:.3f}$")
            st.write(f"Multiple correlation coefficient $R_{{1.23}}$: ${R1_23:.3f}$")

        except Exception as e:
            st.error(f"Error: {e}")
            st.write("Please ensure the data is in the correct format.")