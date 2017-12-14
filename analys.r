setwd("/home/nithin/edu/freedman/wildedatacode/MW-Final-Code-0308/temp/")
wilde<-read.csv("Complexity_Data.csv", header = TRUE)
wilde2 <- wilde[,3:144]
#levels(wilde$Q_N)<-0:1
di<-dist(wilde2, method="euclidean")
fit <- hclust(di ,method="ward.D")

pdf(file="dendrogram.pdf", height=500, width=3000)
plot(fit, labels = wilde$Q_N, cex=0.9, hang=-1)
rect.hclust(fit, k=2)
#groups <- cutree(fit, k=2)
#rect.hclust(fit, k=2, border = "Red")

#pdf(file="kmeans.pdf", height=10, width=20)
#km1<-kmeans(di, centers = 2)
#wilde$Q_N <- as.numeric(as.character( wilde$Q_N ))
#plot(wilde$Q_N)
#text(x=wilde$Q_N, labels=wilde$Q_N, col=km1$cluster+1)
#plot(km1$cluster, col=wilde$Q_N)
#plot(wilde2, col =(km1$cluster +1) , main="K-Means result with 2 clusters", pch=20, cex=2)