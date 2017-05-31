# importing stuff
library(phytools)


loadSimilarityMatrix <- function(exp, pID, session, task){
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

vec.cos <- function(v1, v2){
  nominator <- sum(v1 * v2)
  demonimator <- sqrt(sum(v1*v1)) * sqrt(sum(v2*v2))
  return(nominator/demonimator)
}

getValidityNReliability <- function(exp, pID){
  matrix1 <- loadSimilarityMatrix(exp, pID, 1, 'pair')
  matrix2 <- loadSimilarityMatrix(exp, pID, 2, 'pair')
#  reliability.pair <- 1 - vec.cos(as.vector(matrix1), as.vector(matrix2))
  reliability.pair <- skewers(matrix1, matrix2, method = 'unifcorrmat')
  
  pair_matrix <- (matrix1+matrix2)/2
  
  matrix1 <- loadSimilarityMatrix(exp, pID, 1, 'multi')
  matrix2 <- loadSimilarityMatrix(exp, pID, 2, 'multi')
#  reliability.multi <- 1 - vec.cos(as.vector(matrix1), as.vector(matrix2))
  reliability.multi <- skewers(matrix1, matrix2, method = 'unifcorrmat')
  
  multi_matrix <- (matrix1+matrix2)/2
  
#  validity <- 1 - vec.cos(as.vector(pair_matrix), as.vector(multi_matrix))
  validity <- skewers(multi_matrix, pair_matrix, method = 'unifcorrmat')
  
  return(c(validity$r, validity$p, reliability.pair$r, reliability.pair$p, reliability.multi$r, reliability.multi$p))
}

getData <- function(exp, participants){
  data <- matrix(data = NA, nrow = length(participants), ncol = 7)
  for (pID in participants){
    data[pID,] <- c(pID, getValidityNReliability(exp, pID))
  }
  data <- data.frame(data)
  names(data) <- c('ID', 'Validity_R', 'Validity_P', 'Reliability_Pair_R', 'Reliability_Pair_P', 'Reliability_Multi_R', 'Reliability_Multi_P')
  data$ID <- factor(data$ID)
  
  return(data)
}

exp1.data <- getData(1, c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
exp2.data <- getData(2, c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))