import numpy as np
import random
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.circuit.library import QFT
import matplotlib.pyplot as plt

def create_circuit(num_qubits, T, error_range=0.1):
    """Creates a quantum circuit for period estimation with simulated error.

    Args:
        num_qubits (int): Number of qubits.
        T (float): Real period.
        error_range (float): Range of random error, relative to T.

    Returns:
        QuantumCircuit: The quantum circuit.
    """
    qc = QuantumCircuit(num_qubits, num_qubits)
    qc.h(range(num_qubits))

    for qubit in range(num_qubits):
        error = random.uniform(-error_range * T, error_range * T)
        theta = 2 * np.pi * (2**qubit) / (2**num_qubits)
        qc.p((T + error) * theta, qubit)

    qc.append(QFT(num_qubits, inverse=True), range(num_qubits))
    qc.measure_all()

    return qc

def simulate_circuit(qc, shots=1024):
    """Simulates the given quantum circuit.

    Args:
        qc (QuantumCircuit): The quantum circuit to simulate.
        shots (int): The number of times to run the simulation.

    Returns:
        dict: The counts of the measured results.
    """
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    job = simulator.run(compiled_circuit, shots=shots)
    result = job.result()
    counts = result.get_counts(qc)
    return counts

def plot_results(counts):
    """Plots the results of the simulation.

    Args:
        counts (dict): The counts of the measured results.
    """
    plt.figure(figsize=(10, 6))
    plt.bar(counts.keys(), counts.values())
    plt.xlabel("Measured Value")
    plt.ylabel("Counts")
    plt.title("Quantum Period Estimation Results")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    num_qubits = 8
    T = 3.5  # Example period
    qc = create_circuit(num_qubits, T)
    counts = simulate_circuit(qc)
    plot_results(counts)



