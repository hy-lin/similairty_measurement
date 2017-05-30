library(BayesFactor)


loadTrialData <- function(exp, pID, session, task){
  if (task == 'pair'){
    sim_matrix <- as.matrix(read.table(sprintf('Data/Experiment%d/TrialsDetail/PairWise_%03d_%02d.dat', exp, pID, session), sep = '\t'))
    # trim off the last column
    sim_matrix <- sim_matrix[,-ncol(sim_matrix)]
  }
  else{
    sim_matrix <- as.matrix(read.table(sprintf('Data/Experiment%d/TrialsDetail/MultiItemsArrangement_%03d_%02d.dat', exp, pID, session), sep = '\t'))
    # trim off the last column
    sim_matrix <- sim_matrix[,-ncol(sim_matrix)]
  }
  return(sim_matrix)
}


getData <- function(exp, participants, task){
  if (task == 'pair'){
    data <- matrix(data = NA, nrow = 0, ncol = 6)
    for (pID in participants){
      data <- rbind(data, cbind(pID, loadTrialData(exp, pID, 1, 'pair')))
    }
    data <- data.frame(data)
    names(data) <- c('ID', 'TrialInd', 'ItemL', 'ItemR', 'Similarity', 'RT')
    data$ID <- factor(data$ID)
    data$TrialInd <- factor(data$TrialInd)
    data$ItemL <- factor(data$ItemL)
    data$ItemR <- factor(data$ItemR)
  }
  else{
    data <- matrix(data = NA, nrow = 0, ncol = 27)
    for (pID in participants){
      data <- rbind(data, cbind(pID, loadTrialData(exp, pID, 1, 'multi')))
    }
    data <- data.frame(data)
    names(data) <- c('ID', 'TrialInd', 'Item1', 'x1', 'y1'
                     , 'Item2', 'x2', 'y2'
                     , 'Item3', 'x3', 'y3'
                     , 'Item4', 'x4', 'y4'
                     , 'Item5', 'x5', 'y5'
                     , 'Item6', 'x6', 'y6'
                     , 'Item7', 'x7', 'y7'
                     , 'Item8', 'x8', 'y8'
                     , 'RT')
    data$ID <- factor(data$ID)
    data$TrialInd <- factor(data$TrialInd)
    data$Item1 <- factor(data$Item1)
    data$Item2 <- factor(data$Item2)
    data$Item3 <- factor(data$Item3)
    data$Item4 <- factor(data$Item4)
    data$Item5 <- factor(data$Item5)
    data$Item6 <- factor(data$Item6)
    data$Item7 <- factor(data$Item7)
    data$Item8 <- factor(data$Item8)
  }
  return(data)
}

exp1.pair.data <- getData(1, c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10), 'pair')
exp1.multi.data <- getData(1, c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10), 'multi')

exp1.RT.pair <- data.frame(aggregate(list(exp1.pair.data$RT), list(exp1.pair.data$ID), sum))
exp1.RT.multi <- data.frame(aggregate(list(exp1.multi.data$RT), list(exp1.multi.data$ID), sum))

exp1.RT <- exp1.RT.multi
exp1.RT[, 3] <- exp1.RT.pair[, 2]
names(exp1.RT) <- c('ID', 'MultiRT', 'PairRT')

samples = ttestBF(exp1.RT$MultiRT - exp1.RT$PairRT, posterior = TRUE, iterations = 1000)
plot(samples[, 'mu'])
