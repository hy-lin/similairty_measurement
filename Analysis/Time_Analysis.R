library(BayesFactor)


loadTrialData <- function(exp, pID, session, task){
  if (task == 'pair'){
    sim_matrix <- as.matrix(read.table(sprintf('Data/Experiment%d/SimilarityMatrix/PairWise_%03d_%02d.dat', exp, pID, session), sep = '\t'))
    # trim off the last column
    sim_matrix <- sim_matrix[,-ncol(sim_matrix)]
    sim_matrix <- sim_matrix / 8
  }
  else{
    sim_matrix <- as.matrix(read.table(sprintf('Data/Experiment%d/SimilarityMatrix/MultiItemsArrangement_%03d_%02d.dat', exp, pID, session), sep = '\t'))
    # trim off the last column
    sim_matrix <- sim_matrix[,-ncol(sim_matrix)]
    sim_matrix <- sim_matrix / max(sim_matrix)
  }
  return(sim_matrix)
}