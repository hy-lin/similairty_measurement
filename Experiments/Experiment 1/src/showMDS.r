setwd('D:/Users/Hsuan-Yu Lin/Documents/GitHub/similairty_measurement/Experiments/Experiment 1/src/Data')


readinteger <- function()
{ 
  n <- readline(prompt="Enter participant ID: ")
  return(as.integer(n))
}

pID <- readinteger()

pair_dist_matrix <- as.matrix(read.table(sprintf('PairWise_%03d.dat', pID), sep = '\t'))
pair_dist_matrix <- pair_dist_matrix[,-ncol(pair_dist_matrix)]

pair_loc <- cmdscale(pair_dist_matrix)
pair.scale <- 1/(max(pair_loc)-min(pair_loc))
x = pair_loc[, 1] * pair.scale
y = pair_loc[, 2] * pair.scale

plot(x, y, type = 'n')
text(x, y, colnames(pair_dist_matrix), cex=.6, col = 'red')

multi_dist_matrix <- as.matrix(read.table(sprintf('MultiCompare_%03d.dat', pID), sep = '\t'))
multi_dist_matrix <- multi_dist_matrix[,-ncol(multi_dist_matrix)]

multi_loc <- cmdscale(multi_dist_matrix)
multi.scale <- 1/(max(multi_loc) - min(multi_loc))
x = multi_loc[, 1] * multi.scale
y = multi_loc[, 2] * multi.scale

text(x, y, colnames(multi_dist_matrix), cex=.6, col = 'black')
