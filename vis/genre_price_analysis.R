library(plyr)

# NB: genre_prices.txt contains the farthings per page
# for octavo records only (to control for two significant)
# variables

# Read in the prices associated with each genre label
genre.df <- read.table("genre_prices.txt", sep="\t")
colnames(genre.df) <- c("genre","normalized_price")

# Find counts of each level within the V1 factor
counts.df <- as.data.frame(table(genre.df$genre))

# Examine only those records with 10 or more price observations
subset.df <- subset(counts.df, Freq > 9)
colnames(subset.df) <- c("genre","Freq")

# Plot the observations
# Remove Early Works to 1800 because it's the catchall group
# Remove farthings_per_page > 3 because there are only 3 observations
p <- ggplot( subset(genre.df, genre %in% subset.df$genre & genre != "Early works to 1800" & normalized_price < 3),
  aes( reorder(genre, normalized_price, FUN=median), normalized_price, color=as.factor(reorder(genre, normalized_price, FUN=median)))) +
  geom_jitter(alpha=.3) +
  geom_boxplot(outlier.shape = NA) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  guides(colour=FALSE) +
  xlab("Subject Label") +
  ylab("Farthings Per Page") +
  ggtitle("Normalized Price Distributions by Subject")

ggsave(p, file="price_by_subject.png")
  