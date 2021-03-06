# Create a scatterplot of price vs carat
# and omit the top 1% of price and carat
# values.


ggplot(data = diamonds, aes(x = carat, y = price)) +
    geom_point() +
    scale_x_continuous(limits = c(0, quantile(diamonds$carat, 0.99))) +
    scale_y_continuous(limits = c(0, quantile(diamonds$price, 0.99))) +
    xlab("carat") +
    ylab("price")


quantile(diamonds$carat, .99)

