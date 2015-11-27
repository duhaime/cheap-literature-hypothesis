ecco.df <- read.table("ecco_price_metadata.txt",
                                  sep="\t",
                                  comment.char = "",
                                  quote="")

colnames(ecco.df) <- c("estc_id", "holding_libraries", "document_type", "language", "author", "author_death", "full_title", "title_length", "current_volume", "total_volumes", "publication_city")

# Merge ecco metadata into estc df
estc_ecco.df <- merge(df, ecco.df, by="estc_id")

############################
# Price variance  by author#
############################

# Produce author counts
counts.df <- as.data.frame(table(estc_ecco.df$author.y))

# Examine only those records with 10 or more price observations
subset.df <- subset(counts.df, Freq > 3)
colnames(subset.df) <- c("author","Freq")

p <- ggplot( subset(estc_ecco.df, author.y %in% subset.df$author & author.y != "None"),
             aes( reorder(author.y, farthings_per_page, FUN=median), farthings_per_page, color=as.factor(reorder(author.y, farthings_per_page, FUN=median)))) +
  geom_jitter(alpha=.3) +
  geom_boxplot(outlier.shape = NA) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  guides(colour=FALSE) +
  xlab("Author") +
  ylab("Farthings Per Page") +
  ggtitle("Normalized Price Distributions by Author")

ggsave(p, file="author_prices.png")

##########################################
# Price variance by publication location #
##########################################

# Produce location counts
counts.df <- as.data.frame(table(estc_ecco.df$publication_city))

# Examine only those records with 10 or more price observations
subset.df <- subset(counts.df, Freq > 3)
colnames(subset.df) <- c("publication_city","Freq")

p <- ggplot( subset(estc_ecco.df, publication_city %in% subset.df$publication_city & farthings_per_page < 10 & !grepl("]", publication_city)),
             aes( reorder(publication_city, farthings_per_page, FUN=median), farthings_per_page, color=as.factor(reorder(publication_city, farthings_per_page, FUN=median)))) +
  geom_jitter(alpha=.3) +
  geom_boxplot(outlier.shape = NA) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  guides(colour=FALSE) +
  xlab("Publication City") +
  ylab("Farthings Per Page") +
  ggtitle("Normalized Price Distributions by Publication Location")

ggsave(p, file="location_prices.png")

##############################
# Price variance by language #
##############################

# Produce language counts
counts.df <- as.data.frame(table(estc_ecco.df$language))

# Examine only those records with 10 or more price observations
subset.df <- subset(counts.df, Freq > 3)
colnames(subset.df) <- c("language","Freq")

p <- ggplot( subset(estc_ecco.df, language %in% subset.df$language & farthings_per_page < 10),
             aes( reorder(language, farthings_per_page, FUN=median), farthings_per_page, color=as.factor(reorder(language, farthings_per_page, FUN=median)))) +
  geom_jitter(alpha=.3) +
  geom_boxplot(outlier.shape = NA) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  guides(colour=FALSE) +
  xlab("Publication City") +
  ylab("Farthings Per Page") +
  ggtitle("Normalized Price Distributions by Publication Location")

ggsave(p, file="location_prices.png")
