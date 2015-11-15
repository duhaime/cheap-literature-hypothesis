library(ggplot2)

# Set workding directory to data location
setwd("../data/")

# Read dataframe
df <- read.table("clustered_estc_price_data.txt", 
                 sep="\t", 
                 quote='"',
                 fill=NA,
                 na.strings='NULL',
                 colClasses = c('character','numeric','character','numeric','character', 'numeric',
                                rep('character',3), rep('numeric',3), rep('character',2), rep('numeric',3), 'character')
                 )

# Provide column headers
colnames(df) <- c("estc_id","year","raw_size","clean_size","raw_pages","clean_pages","notes","raw_price","parsed_price","pence","illustrations","farthings_per_page","author","title","ignore","cluster","unique_years_in_cluster","canonical_title")

##################################
# Plot Selected Prices over Time #
##################################

# Populate prices for just nine titles, 3 with + slope, 3 with - slope, and 3 with vertical line
nine_titles <- c("The historical register,", "John Bull in his senses:", "The compleat housewife:", "The grave. A poem.", "Cadenus and Vanessa.", "Kent's directory", "The london songster; or polite musi", "Sketches from nature,", "The shopkeeper's and tradesman's as")

#shorten the titles so trailing whitespace doesn't crush the ggplot guide/legend
df$short_title <- strtrim(df$title, 35)

# Rearrange the order of these values so that we can plot in the desired order
sample_prices <- subset(df, short_title %in% nine_titles)
sample_prices$facet_order <- factor(sample_prices$short_title, levels = c("The historical register,", "John Bull in his senses:", "The compleat housewife:", "The grave. A poem.", "Cadenus and Vanessa.", "Kent's directory", "The london songster; or polite musi", "Sketches from nature,", "The shopkeeper's and tradesman's as"))

#change name of book price in dataframe
sample_prices$clean_size[sample_prices$clean_size == 4] <- "quarto"
sample_prices$clean_size[sample_prices$clean_size == 8] <- "octavo"
sample_prices$clean_size[sample_prices$clean_size == 12] <- "duodecimo"

ggplot(sample_prices, aes(x=as.numeric(as.character(year)),y=as.numeric(as.character(farthings_per_page)),colour=as.factor(clean_size))) +
  geom_jitter() +
  facet_wrap(~facet_order, ncol=3, scales="free_y") +
  geom_smooth(method="lm") +
  xlab("Year") +
  ylab("Farthings per Page") +
  ggtitle("The Changing Price of Eighteenth-Century Texts") +
  scale_colour_discrete(name="Book Size")

####################
# Plot Book Facets #
####################

# Shorten title for display purposes
df$title_to_plot <- paste( substr(df$canonical_title,0,15), "..." ) 

# Plot all instances of each book as a unique facet 
ggplot(subset(df, unique_years_in_cluster > 2), aes(x=year,y=farthings_per_page, colour=as.factor(cluster))) +
  geom_point() +
  stat_smooth(method="lm") +
  facet_wrap(~title_to_plot, ncol=10) +
  scale_x_continuous() +
  scale_y_continuous(limits=c(0,3)) +
  scale_colour_discrete(guide=FALSE)





# If we take the mean of all slopes for each position along the x axis, we can measure aggregate trajectories
