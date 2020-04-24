# First attempt at plotting K279a pH gradient experiment
# loading in libraries
# updated 9-27-19
require(ggplot2)
# load in data
DATA <- read.csv(file = "/Volumes/GoogleDrive/My Drive/UG_Stenotrophomonas_Antibiotics/data/raw/ALLdata.csv",
                 header=T)

Tara.DATA <- read.csv(file="/Volumes/GoogleDrive/My Drive/StenoAntibiotics/Steno_Growth.csv")
Tara.DATA$X <-c(1:nrow(Tara.DATA))
Tara.DATA$PredetMIC<-c(16)
Tara.DATA$Oxygen <- c("aerobic")
colnames(Tara.DATA)[which(colnames(Tara.DATA)=="Timepoint")] <- c("Incubation")
Tara.DATA$Person <- c("Tara")
Tara.DATA$ConcFormat <- c("")
Tara.DATA$pH <- as.character(Tara.DATA$pH)
Tara.DATA$pH <- paste("pH", Tara.DATA$pH, sep="")



DATA$Incubation<- as.character(DATA$Incubation)
Tara.DATA$Incubation<- as.character(Tara.DATA$Incubation)
Tara.DATA$Incubation <- paste(Tara.DATA$Incubation,"hr", sep="")

Tara.DATA$Antibiotic <- gsub(pattern="Levofloxacin", replacement="levofloxacin", Tara.DATA$Antibiotic)

DATA <- rbind(DATA,Tara.DATA)

# calculate the average per concentration, pH, strain, and incubation
require(dplyr)
avg.OD <- DATA%>% group_by(Strain, pH, Concentration, Antibiotic, Incubation,Oxygen) %>%
  summarise(meanOD=mean(OD))
#scatter plot with white background, black lines and text theme
ggplot() +
  geom_point(data=subset(DATA), aes(x=as.numeric(as.character(Concentration)), y=OD, fill=as.factor(pH), shape=as.factor(pH)), color="black")+
  geom_line(data=subset(avg.OD), aes(x=as.numeric(as.character(Concentration)), y=meanOD, color=as.factor(pH)))+
  facet_grid(vars(Incubation, Strain, Oxygen), scale="free_x")+
  #theme chunk will give white background and black text/lines for all plot elements
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
              axis.line = element_line(colour = "black"),
              axis.title = element_text(size=16),
              axis.text=element_text(size=14,colour="black"),
              panel.background=element_rect(color="black", fill="white"),
              strip.background = element_rect(color="black", fill="white"),
              strip.text.y=element_text(),
              legend.text=element_text( color="black"),
              legend.background = element_rect(fill="white", color="white"),
              legend.key = element_rect(fill="white", color="white"))+
  # use different colors
  scale_color_manual(values = c("orange", "gray", "purple"), name="pH")+
  scale_fill_manual(values = c("orange", "gray", "purple"), name="pH")+
  scale_shape_manual(values=c(21,22,23), name="pH")+
  geom_vline(data=DATA, aes(xintercept = as.numeric(as.character(PredetMIC))), linetype="dashed") +
  xlab("Concentration mg/L")

#box plot with same colors as scatter plot above
ggplot() +
  geom_boxplot(data=DATA, 
               aes(x=as.numeric(as.character((Concentration))), 
                   y=OD,color=as.factor(pH), fill=as.factor(pH), group=interaction(Concentration, pH, Strain)))+
  facet_grid(Incubation~Strain, scales="free")+
  #theme chunk will give white background and black text/lines for all plot elements
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        axis.line = element_line(colour = "black"),
        axis.title = element_text(size=16),
        axis.text=element_text(size=14,colour="black"),
        panel.background=element_rect(color="black", fill="white"),
        strip.background = element_rect(color="black", fill="white"),
        strip.text.y=element_text(size=12),
        legend.text=element_text(size=12, color="black"),
        legend.background = element_rect(fill="white", color="white"),
        legend.key = element_rect(fill="white", color="white"),
        strip.text=element_text(color="black",size=16))+
  # use different colors
  # note, have to use FILL if you want boxplot shades with diff colors
  scale_fill_manual(values = c("orange", "black", "purple"), name="pH")+
  #make border same colors as fill
  scale_color_manual(values=c("orange", "black", "purple"), name="pH")+
  # change x axis label
  xlab("Concentration (mg/L)")+
  geom_vline(data=DATA, aes(xintercept = as.numeric(as.character(PredetMIC))), linetype="dashed") 

