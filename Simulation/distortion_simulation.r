library(phytools)
library('gtools')
library('ggplot2')
library('reshape2')

source('core_functions.r')

simMIRTValidity <- function(stimuli, n_in_subsets, true_similarity_matrix = NA){
  n_stimuli <- dim(stimuli)[1]
  if (anyNA(true_similarity_matrix)){
    true_similarity_matrix <- getSimilarityMatrix(stimuli)
  }
  
  measured_similarity_matrix <- matrix(0, n_stimuli, n_stimuli)
  n_measurement <- matrix(0, n_stimuli, n_stimuli)
  
  subsets <- getSubsets(n_stimuli, n_in_subsets)
  subset_pairs <- combinations(length(subsets), 2)
  
  for (pair_index in seq(dim(subset_pairs)[1])){
    current_stimuli <- c(subsets[[subset_pairs[pair_index, 1]]], subsets[[subset_pairs[pair_index, 2]]])
    sub_similarity_matrix <- true_similarity_matrix[current_stimuli, current_stimuli]
    MIS_result <- cmdscale(sub_similarity_matrix, k = min(2, length(current_stimuli)-1))
    measured_sub_similarity_matrix <- getSimilarityMatrix(MIS_result)
    measured_similarity_matrix[current_stimuli, current_stimuli] <- measured_similarity_matrix[current_stimuli, current_stimuli] + measured_sub_similarity_matrix
    n_measurement[current_stimuli, current_stimuli] <- n_measurement[current_stimuli, current_stimuli] + 1
  }
  
  measured_similarity_matrix <- measured_similarity_matrix / n_measurement
  return(skewers(true_similarity_matrix, measured_similarity_matrix)$r)
}

n_iter <- 100
n_stimuli <- 32
ns_dimension <- seq(2, 32, by = 2)
ns_in_subsets <- seq(1, ceiling(n_stimuli/2))
representation_noise = 0.05
validity <- matrix(0, length(ns_dimension), length(ns_in_subsets))
rs <- matrix(0, n_iter, ceiling(n_stimuli/2))

for (dim_index in seq(1, length(ns_dimension))){
  n_dimension <- ns_dimension[dim_index]
  print(c('working on ', n_dimension, 'dimension'))
  
  for (i in seq(n_iter)){
    stimuli <- createStimuli(n_stimuli, n_dimension, representation_noise)
    true_similarity_matrix <- getSimilarityMatrix(stimuli)
    for (n_index in seq(1, length(ns_in_subsets))){
      n_in_subsets <- ns_in_subsets[n_index]
      rs[i,n_index] <- simMIRTValidity(stimuli, n_in_subsets, true_similarity_matrix)    
    }
  }
  validity[dim_index, ] <- colMeans(rs)
}
validity <- as.data.frame(validity)
names(validity) <- c('n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'n7', 'n8')
validity$n_dim <- ns_dimension
validity <- melt(validity, id = 'n_dim', variable.name = 'n_subsets', value.name = 'validity')

pd <- position_dodge(.1)
ggplot(data=validity) + aes(x=n_dim, y = validity, linetype = n_subsets, group = n_subsets) + 
  geom_line(position = pd) + 
  geom_point(position = pd)
