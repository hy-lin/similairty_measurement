createStimuli <- function(n_stimuli, n_dimension = NA, noise_sd = 0.05){
  if (is.nan(n_dimension)){
    n_dimension <- n_stimuli
  }
  
  stimuli <- matrix(0, n_stimuli, n_dimension)
  
  for (stimulus_index in seq(n_stimuli)){
    stimuli[stimulus_index, ] <- sign(runif(n_dimension) - 0.5)
  }
  stimuli <- stimuli + rnorm(n_dimension*n_stimuli, mean = 0, sd = noise_sd)
  return(stimuli)
}

getSimilarity <- function(stimulus_one, stimulus_two){
  return(sqrt(sum((stimulus_one - stimulus_two)^2)))
}

getSimilarityMatrix <- function(stimuli){
  n_stimuli <- dim(stimuli)[1]
  sim_matrix <- matrix(0, n_stimuli, n_stimuli)
  for (stimulus_one in seq(n_stimuli)){
    for (stimulus_two in seq(n_stimuli)){
      sim_matrix[stimulus_one, stimulus_two] <- getSimilarity(stimuli[stimulus_one, ], stimuli[stimulus_two, ])
    }
  }
  return(sim_matrix)
}


getSubsets <- function(n_stimuli, n_stimuli_in_subsets){
  n_subsets <- ceiling(n_stimuli / n_stimuli_in_subsets)
  n_in_subsets <- rep(n_stimuli_in_subsets, n_subsets)
  if (n_stimuli %% n_stimuli_in_subsets != 0){
    unavaliable_items <- n_stimuli_in_subsets - n_stimuli %% n_stimuli_in_subsets
    n_in_subsets <- n_in_subsets - unavaliable_items %/% n_subsets
    if (unavaliable_items %% n_subsets != 0){
      n_in_subsets[1:unavaliable_items %% n_subsets] <- n_in_subsets[1:unavaliable_items %% n_subsets] - 1
    }
  }
  subsets <- list()
  current_item = 1
  for (i in seq(n_subsets)){
    subsets[[i]] <- seq(current_item, current_item + n_in_subsets[i]-1)
    current_item <- current_item + n_in_subsets[i]
  }
  return(subsets)
}
