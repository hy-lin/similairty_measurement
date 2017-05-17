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

plotMDS <- function(exp, participants){
  pair_matrix <- matrix(data = 0, nrow = 16, ncol = 16)
  multi_matrix <- matrix(data = 0, nrow = 16, ncol = 16)
  for (pID in participants){
    pair_matrix <- pair_matrix + loadSimilarityMatrix(exp, pID, 1, 'pair')
    pair_matrix <- pair_matrix + loadSimilarityMatrix(exp, pID, 2, 'pair')
    
    multi_matrix <- pair_matrix + loadSimilarityMatrix(exp, pID, 1, 'multi')
    multi_matrix <- pair_matrix + loadSimilarityMatrix(exp, pID, 2, 'multi')
  }
  
  pair_matrix <- pair_matrix / length(participants) / 2
  multi_matrix <- multi_matrix / length(participants) / 2
  
  multi_loc <- cmdscale(multi_matrix)
  multi.scale <- 1.5/(max(multi_loc) - min(multi_loc))
  multi.x = multi_loc[, 1] * multi.scale
  multi.y = multi_loc[, 2] * multi.scale
  
  plot(multi.x, multi.y, type = 'n', xlim = c(-1, 1), ylim = c(-1, 1))
  text(multi.x, multi.y, colnames(multi_matrix), cex=.6, col = 'black')
  
  pair_loc <- cmdscale(pair_matrix)
  pair.scale <- 1.5/(max(pair_loc)-min(pair_loc))
  pair.x = pair_loc[, 1] * pair.scale
  pair.y = pair_loc[, 2] * pair.scale
  
  pair.x <- pair.x * sign(pair.x[1] * multi.x[1]) 
  pair.y <- pair.y * sign(pair.y[1] * multi.y[1])
  
  #plot(pair.x, pair.y, type = 'n', xlim = c(-1, 1), ylim = c(-1, 1))
  text(pair.x, pair.y, colnames(pair_matrix), cex=.6, col = 'red')
}

plotMDS(1, c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
plotMDS(2, c(1, 2, 3, 4, 5, 6, 7, 8, 9))