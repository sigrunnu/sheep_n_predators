library(PBSmapping)
library(adehabitatHR)    #?
options(stringsAsFactors=F)


  

#################################################### #########################################################

  ## mappa hvor du henter din fil
  setwd("S:\\Prosjekter\\tinVilt\\M_Prosjekt_Hjort\\Data\\Posisjoner_areal\\data_areal_210401")


  
 ## Leser inn ei fil , denne som txt fil hvor alle id'en er samlet i ei fil'
alle<-read.table("datafila.txt",h=T,sep="\t",dec=".")


# Fordel at id kolonna står i Character format
alle$id=as.character(alle$id)
 options(stringsAsFactors=FALSE)

 # Lager en datotime kolonna til et format som R synes er greit å jobbe med
 
 alle$datetime<-as.POSIXct(strptime(alle$datetime,format="%Y-%m-%d %H:%M:%S"),tz="") 



   alle<-alle[order(alle$id,alle$datetime),]



#-------------------------------------------------------------------------
# Remove data points up to 24 hours after marking and after date of death
#-------------------------------------------------------------------------


utin<-read.table("covariates_om_dyrene.txt",h=T,sep="\t",dec=".")



# Tar ut de relevante kolonnene foreløpig!

   utin<-utin[,c(2,4:10,31:36)]
   
   ## Datoformat??   - MÅ GJØRE OM DATETIME TIL as.POSIXct format      NBNBNBN  i utin (covariat fila)
 
 # Setter alle verdier av na for marktime til kl 23:00
       utin$marktime[is.na(utin$marktime)]="23:00"
 
dati<-paste(utin$markdate,utin$marktime) 
 utin$firstdate<-as.POSIXct(strptime(dati,format="%d.%m.%Y %H:%M"))
                                
                                                    
#          firstdate=ifelse(is.na(utin$markdate),"2002-01-01",utin$markdate) # add fake early marking date to those with missing value
    
#    utin$firstdate2<-as.POSIXct(strptime(markdate,format="%Y-%m-%d ",tz=""))       #%# Det skjer etter eller annet her slik at firstdate2 kommer kun som NA, det er kun de som er 
    #skrevet med 01.01.2002 som kommer med. Betyr at det er noe med datoformatet som er gæli her.
 
  #  lastdate=ifelse(is.na(utin$collarstopdate),"2020-01-01",utin$collarstopdate)  # add fake late date to those with missing value for last position
 
 
 # Setter verdier av na - altså halsbånd som ennå er i drift til 01.01.2030
    utin$collarstopdate[is.na(utin$collarstopdate)]="01.01.2030"
  
 #   utin$marktime[is.na(utin$marktime)]="23:00"
 
 dati<-paste(utin$collarstopdate) 
    utin$lastdate<-as.POSIXct(strptime(dati,format="%d.%m.%Y"))       
 

    
## Merge with data set alle
    alle1=merge(alle,utin,by.x="id",by.y="id",all.x=T,sort=T,suffixes=c("",".y"))        #   

 

    # Remove fixes obtained before marking and the first 24 hour after marking
          # NB Nytt opplegg - tar med alle også på merkedag.
    timediff=difftime(alle1$datetime,alle1$firstdate,tz="",units="hours")                                               # 
    alle2=alle1[timediff>0,]   # 22 instead of 24 because collar time is GMT while marktime is Norwegian winter time    # 
    # check:
    range(difftime(alle2$datetime,alle2$firstdate),na.rm=T)

    # Remove fixes obtained after death/last valid location
    timediff1=difftime(alle2$lastdate,alle2$datetime,tz="",units="hours")
    alle3=alle2[timediff1>0,]
    # check:
    range(difftime(alle3$lastdate,alle3$datetime,tz="",units="hours"),na.rm=T)                                            # 


 
#-------------------------------------------------------------------------
#Check for duplicated locations
#-------------------------------------------------------------------------

#make idtime column. THERE SHOULD NEVER BE >1 UNIQUE ENTRY!!!
alle3$idtime=paste(alle3$id,alle3$datetime,sep="_")

#Check this
idtime=as.data.frame(table(alle3$idtime))

idtime99=idtime[idtime$Freq>5,]

#How many have more than one unique entry?
idtime2=idtime[idtime$Freq>1,]
dim(idtime2)

#check dims and how many you should end up with
#Number entries that should be removed
sum(idtime2$Freq)-length(idtime2$Freq)
#check pos too
length(alle3$idtime)-length(unique(alle3$idtime))
#this is the number of entries to remove

#subset only unique values of idtime
alle3$idtime=as.factor(as.character(alle3$idtime))  #subsetting is faster when using factor than when using character!!
alle4=subset(alle3, !duplicated(alle3$idtime))      #this is the number of entries to remove     





#----------------------------#
### Convert lat long to UTM
#----------------------------#

# Dette trengs ikke å kjøres hvis posisjonsformatet allerede er i UTM

alle4$lat<-(as.numeric(as.character(alle4$lat)))
alle4$long<-(as.numeric(as.character(alle4$long)) )

#NB NB NB. alle3 still contains NA values for east and north. Merge bak with this later

   plot(alle4$long,alle4$lat)
 range(alle4$lat)
 
# First need to overwrite some odd lat and long (otherwise southern hemisphere is assumed)
 tull=subset(alle4,(lat>63.5))
 
 alle4$lat[alle4$lat<0]=NA
alle4$long[alle4$long<0]=NA

  
   plot(alle4$long,alle4$lat)
### Pga feilmelding i van moorter screening fjerner jeg noen av de største feilene manuelt:
#    alle4$long[alle4$long<5.5]=NA
 #     alle4$long[alle4$long>12]=NA
 #       alle4$lat[alle4$lat<59]=NA
        alle4$lat[alle4$lat>63.5]=NA  
# Need to exclude NAs before converting     NB Fila alle4 inneholder dermed også NA verdier for 
alle5<-subset(alle4,is.na(lat)!=T)                       # 
alle5<-subset(alle5,is.na(long)!=T)                                          # 

    plot(alle5$long,alle5$lat)


latlong=data.frame(EID=1:nrow(alle5),X=alle5$long,Y=alle5$lat)

range(alle5$lat)
range(alle5$long)        #  

library(PBSmapping)
#library(adehabitat)

latlong=as.EventData(latlong, projection = "LL", zone = NULL)
attr(latlong, "zone") <- 32  #manually set the UTM zone - 32 for Norway
UTM <- convUL(latlong,km=F) #convert from latlong to UTM

alle5$east<-UTM$X
alle5$north<-UTM$Y

### Pga feilmelding i van moorter screening fjerner jeg noen av de største feilene manuelt:
  #  alle5$east[alle5$east<360000]=NA
   # alle5$north[alle5$north<0]=NA
  # alle5$north[alle5$north<6600000]=NA
  #  alle5$north[alle5$north>7100000]=NA
   # alle5$east[alle5$east>1e+06]=NA
     
    plot(alle5$east,alle5$north)
    
    # In addition: delete individuals with less than 10 GPS locations:
    # 
     
#   

#    ix<-alle4$id %in% rem
 #   table(ix)
#    table(tmp$id)
    
#alle5<-alle4[!ix,]
alle5$id<-as.character(as.factor(alle5$id))
 options(stringsAsFactors=FALSE)
 
 
#-------------------------------------------------------------------------
# van moorter screening
#-------------------------------------------------------------------------
 ## DETTE ER SELVE SCREENINGEN



# Sletter uteliggere med script laget av Bram van Moorter
mydata<-alle5[,c("id","datetime","east","north")]
mydata<-na.omit(mydata) 

table(mydata$id)[order(table(mydata$id))]

mydata$datetime<-as.character(mydata$datetime)

#mydata$datetime<-as.POSIXct(strptime(mydata$datetime,format="%d.%m.%Y",tz=""))
mydata$datetime=as.POSIXct(strptime(mydata$datetime,format="%Y-%m-%d%H:%M:%S"),tz="")


mydata<-mydata[order(mydata$id,mydata$datetime),]
library(adehabitatLT)
library(adehabitatHR)

  setwd("S:\\Prosjekter\\tinVilt\\M_Prosjekt_Hjort\\Data\\Posisjoner_areal\\data_areal_210401")

# LES in scriptet gps_screening_vanMorter.r
source("gps_screening_vanMorter_ny.R")

mydata <- GPS.screening.wrp(mydata$id, mydata$east, mydata$north, mydata$datetime, medcrit=100000, meancrit=10000, spikesp=1500, spikecos=(-0.97))

table(mydata$R1error)        # 
table(mydata$R2error)        # 

# Overkjør med NA i stedet for å slette
mydata2<-mydata
mydata2$y[mydata2$R1error==T]=NA
mydata2$x[mydata2$R1error==T]=NA
mydata2$y[mydata2$R2error==T]=NA
mydata2$x[mydata2$R2error==T]=NA

plot(mydata$x,mydata$y)
points(mydata2$x,mydata2$y,col="red")

### Merge with alle4 in order to keep also NA coordinates (in case of Frair simulation later ###
alle4$match<-paste(alle4$id,alle4$datetime)
mydata2$match<-paste(mydata2$id,mydata2$date)

alle6=merge(alle4,mydata2,by.x="match",by.y="match",all.x=T,sort=T,suffixes=c("",".y"))

plot(alle6$x,alle6$y)
  ## 
  
 

 write.table(alle6,file="oppdatering_pos_renska.txt",col.names=NA,sep="\t")

   
 
save(alle6,file="oppdatering_pos_renska.Rdata")

### ##################################################################################


