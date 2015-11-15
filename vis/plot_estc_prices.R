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
colnames(df) <- c("estc_id","year","raw_size","clean_size","raw_pages","clean_pages","notes","raw_price","parsed_price","farthings","illustrations","farthings_per_page","author","title","ignore","cluster","unique_years_in_cluster","canonical_title")

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
  ggtitle("Price Slopes for Selected Eighteenth-Century Texts") +
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

########################################
# Plot farthings per page by book size #
########################################

# Calculate number of estc ids per condition (clean_size*year)
n_mean_sd_by_size<- aggregate(df["estc_id"], by=df[c("clean_size","year")], FUN=length)

# Change colname of the number of estc ids per condition to "N"
names(n_mean_sd_by_size)[names(n_mean_sd_by_size)=="estc_id"] <- "N"

# Calculate mean price of books for each size and year combination
mean_by_size.df <- aggregate(farthings_per_page ~ year + clean_size, data = subset(df, clean_pages > 20 ), FUN = 'mean')

# Change colname of the mean price per size and year combination
names(mean_by_size.df)[names(mean_by_size.df)=="farthings_per_page"] <- "mean"

# Merge the dataframes
n_mean_sd_by_size <- merge(n_mean_sd_by_size, mean_by_size.df)

# Get the sample (n-1) standard deviation for farthings_per_page ~ each size and year combination
sd_by_size.df <- aggregate(farthings_per_page ~ year + clean_size, data = subset(df, clean_pages > 20 ), FUN = 'sd')

# Change the colname of the sd per size and year combination
names(sd_by_size.df)[names(sd_by_size.df)=="farthings_per_page"] <- "sd"

# Merge the sd into n_mean_sd_by_size
n_mean_sd_by_size <- merge(n_mean_sd_by_size, sd_by_size.df)

# Retrieve wage data from Wrigley and Schofield
wage_data.df <- read.table('wrigley_schofield_six_forty_farthings.txt')

# Rename wage data columns (use colheaders of good_sizes for easy dataframe concatenation)
colnames(wage_data.df) <- c("year", "clean_size", "mean")

# Take the subset of the wage data pertaining to years 1700-1800
wage_data.df <- subset(wage_data.df, 1699 < year & year < 1801)

# Append fill values for wage data df
wage_data.df$N <- NA
wage_data.df$sd <- NA

# Merge wage data with book price stats
n_mean_sd_by_size <- rbind(n_mean_sd_by_size, wage_data.df)

# Rename book sizes for clarity
n_mean_sd_by_size$size[ n_mean_sd_by_size$clean_size == 4 ] <- 'quarto'
n_mean_sd_by_size$size[ n_mean_sd_by_size$clean_size == 8 ] <- 'octavo'
n_mean_sd_by_size$size[ n_mean_sd_by_size$clean_size == 12 ] <- 'duodecimo'
n_mean_sd_by_size$size[ n_mean_sd_by_size$clean_size == 'labour' ] <- 'wrigley labour estimate'

# Plot the aggregated df
ggplot( subset(n_mean_sd_by_size, !is.na(size)), aes(x=year, y=mean, color=size) ) +
  geom_point() +
  geom_smooth() +
  #geom_errorbar( aes(ymin=mean-sd, ymax=mean+sd), width=.1) +
  scale_x_continuous(limits=c(1700, 1800)) +
  facet_wrap(~size, scales="free_y", ncol=1) +
  ylab("Mean Price Per Page") +
  xlab("Year") +
  ggtitle("Mean Price Per Page of English Volumes Within the ESTC") +
  guides(color=FALSE)   # this masks the whole key

# If we take the mean of all slopes for each position along the x axis, we can measure aggregate trajectories
