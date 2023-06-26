using HDF5
using LinearAlgebra
struct Anderson
    energy::Vector{Float64}
    lattice_size::Int64
end
function hamiltonian(energy, lattice_size)
    off_diagonal=ones(lattice_size-1) 
    H=diagm(-1=>off_diagonal,0=>energy,1=>off_diagonal)
    H[lattice_size,1]=1
    H[1,lattice_size]=1
    return H
end
function loschmidt_amplitude(energy, lattice_size, t)
    H=hamiltonian(energy, lattice_size)
    U=expm(-im*H*t)
    return U
end
lattice_size=10                             # lattice size   
W=1                                         # disorder strength
energy=rand(-W/2:1e-10:W/2,lattice_size)      # random energy 
H=hamiltonian(energy,lattice_size)
println(H)
println(loschmidt_amplitude(energy,lattice_size,1))


