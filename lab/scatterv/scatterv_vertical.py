#!/usr/bin/env python

from mpi4py import MPI  # MPI.Init() implicite
import numpy as np

def main():
    """
    Programme principal
    """

    N = 5

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    nranks = comm.Get_size()

    if rank == 0:
        matrice = np.arange(N * N, dtype='float64').reshape(N, N, order='C')
        print(f'Matrice à diviser :\n{matrice}')

        tailles = [p.shape for p in np.array_split(matrice, nranks, axis=0)]
        print(f'Tailles pour {nranks} processus : {tailles}')
    else:
        matrice = None
        tailles = None

    tailles = comm.bcast(tailles)

    n_elements = [t[0] * t[1] for t in tailles]
    portion = np.zeros(tailles[rank])

    comm.Scatterv([matrice, n_elements], portion)

    print(f'Portion du rank {rank} :\n{portion}')

    comm.Gatherv(portion * N, [matrice, n_elements])

    if rank == 0:
        print(f'Matrice finale :\n{matrice}')

    MPI.Finalize()


if __name__ == '__main__':
    main()
