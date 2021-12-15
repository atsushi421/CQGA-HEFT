## read data file
d1 <- read.table("../result/change_CCR/QLHEFT/CCR_0.25.txt")
d1 <- d1$V2
d1_nume <- as.numeric(d1)
d1_median <- median(d1_nume)
d1 <- d1 / d1_median  # QLHEFT_0.25_median
d2 <- read.table("../result/change_CCR/QLHEFT/CCR_0.5.txt")
d2 <- d2$V2
d2_nume <- as.numeric(d2)
d2_median <- median(d2_nume)
d2 <- d2 / d2_median  # QLHEFT_0.5_median
d3 <- read.table("../result/change_CCR/QLHEFT/CCR_1.0.txt")
d3 <- d3$V2
d3_nume <- as.numeric(d3)
d3_median <- median(d3_nume)
d3 <- d3 / d3_median  # QLHEFT_1.0_median
d4 <- read.table("../result/change_CCR/QLHEFT/CCR_2.0.txt")
d4 <- d4$V2
d4_nume <- as.numeric(d4)
d4_median <- median(d4_nume)
d4 <- d4 / d4_median  # QLHEFT_2.0_median
d5 <- read.table("../result/change_CCR/QLHEFT/CCR_4.0.txt")
d5 <- d5$V2
d5_nume <- as.numeric(d5)
d5_median <- median(d5_nume)
d5 <- d5 / d5_median  # QLHEFT_4.0_median
qlheft <- cbind(d1, d2, d3, d4, d5) # bind data

## read data file
d1 <- read.table("../result/change_CCR/Proposed/CCR_0.25.txt")
d1 <- d1$V2
d1 <- d1 / d1_median  # QLHEFT_0.25_median
d2 <- read.table("../result/change_CCR/Proposed/CCR_0.5.txt")
d2 <- d2$V2
d2 <- d2 / d2_median  # QLHEFT_0.5_median
d3 <- read.table("../result/change_CCR/Proposed/CCR_1.0.txt")
d3 <- d3$V2
d3 <- d3 / d3_median  # QLHEFT_1.0_median
d4 <- read.table("../result/change_CCR/Proposed/CCR_2.0.txt")
d4 <- d4$V2
d4 <- d4 / d4_median  # QLHEFT_2.0_median
d5 <- read.table("../result/change_CCR/Proposed/CCR_4.0.txt")
d5 <- d5$V2
d5 <- d5 / d5_median  # QLHEFT_4.0_median
proposed <- cbind(d1, d2, d3, d4, d5) # bind data

## read data file
d1 <- read.table("../result/change_CCR/HEFT/CCR_0.25.txt")
d1 <- d1$V2
d1 <- d1 / d1_median  # QLHEFT_0.25_median
d2 <- read.table("../result/change_CCR/HEFT/CCR_0.5.txt")
d2 <- d2$V2
d2 <- d2 / d2_median  # QLHEFT_0.5_median
d3 <- read.table("../result/change_CCR/HEFT/CCR_1.0.txt")
d3 <- d3$V2
d3 <- d3 / d3_median  # QLHEFT_1.0_median
d4 <- read.table("../result/change_CCR/HEFT/CCR_2.0.txt")
d4 <- d4$V2
d4 <- d4 / d4_median  # QLHEFT_2.0_median
d5 <- read.table("../result/change_CCR/HEFT/CCR_4.0.txt")
d5 <- d5$V2
d5 <- d5 / d5_median  # QLHEFT_4.0_median
heft <- cbind(d1, d2, d3, d4, d5) # bind data

all_data <- list(proposed, qlheft, heft)         # merge two data (data.frame) into a list

## define x-axis scale name
xaxis_scale <- c("0.25", "0.5", "1.0", "2.0", "4,0")
box_cols <- c("pink", "lightcyan", "palegreen1")                # box colors
## border_cols <- c("red", "blue")                   # box-line colrs
border_cols <- c("red", "blue", "palegreen4")                   # box-line colors

## graphic function
comparison_BoxPlot <- function(all_data) {
    ## set parameters for graph
    par(
        xaxs="i",                      # x-axis data span has no margin
        mar = c(5,6,2,2)                #  margin
    )
    ## prepare graph feild
    plot(
        0, 0, type = "n",
        xlab = "CCR", ylab = "Makespan", # labels
        cex.lab = 2,                     # label font size
        font.lab = 1,                      # label font
        xlim = range(0:(ncol(proposed) * 3)), # define large x-axis
        ylim = c(0.2, max(range(proposed), range(qlheft), range(heft))), # y-axis data span
        font.axis = 1,                                # axis font
        cex.axis = 1.5,
        xaxt = "n"                                    # no x-axis
    )
    ## draw vertical line
    abline(
        v = c(3, 6, 9, 12, 15, 18, 21), # position
        lwd = 1,                       # line width
        col = 1,                    # line color
        lty = 1                     # line style
    )
    ## draw boxplot
    for (i in 1:3){
        boxplot(
            all_data[[i]],
            at = c(1:ncol(proposed)) * 3 + i - 3.5, # position of drawing boxplot
            border = border_cols[i],                 # ボックス枠線の色
            col = box_cols[i],                       # colors
            yaxt = "n",
            xaxt = "n",                          # no x-axis scale
            range = 0,                           # no plot outliers 
            add = TRUE)
    }
    ## legend
    legend(
        0.1, 0.65,                      # position
        legend = c("CQGA-HEFT", "CQ-HEFT", "HEFT"),   # labels
        cex = 1.3,                      # labels font size
        pt.cex = 3,                     # marker size
        pch = 22,                       # kinds of marker
        col = border_cols,              # box-line colors
        pt.bg = box_cols,               # box colors
        lty = 0,                               
        lwd = 2,                        # box-line width
        bg = "white"                    # background color
    )
    ## x-axis scale
    axis(
        1,                                    
        at = 1:length(xaxis_scale) * 3 - 1.5, # position of scale
        labels = xaxis_scale,                 # set scale name
        cex.axis=1.5,                        # axis font size
        tick = TRUE                           
    )
}

## output file as eps
postscript("change_CCR_normalization_qlheft_BoxPlot.eps", horizontal = F, onefile = FALSE, paper = "special", width = 8, height = 6)
comparison_BoxPlot(all_data)
dev.off()

## output file as png
png("change_CCR_normalization_qlheft_BoxPlot.png", width = 600, height =400)
comparison_BoxPlot(all_data)
dev.off()