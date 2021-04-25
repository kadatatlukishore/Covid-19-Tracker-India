# Covid-19-Tracker-India

## Covid Help Resources

- http://nixxer.in/covid
- https://kadatatlukishore.github.io/covid-resources.html (More Resources Links)

### Demo Link: 
- https://covid19-india-tracker-and-news.herokuapp.com/
![Alt Text](https://github.com/kadatatlukishore/Covid-19-Tracker-India/blob/main/assets/covid19Tracker-gif.gif)
### Data Sources and References:
- API :  https://api.covid19india.org/data.json
- Dash:  https://dash.plotly.com/

### Directory Tree
```
├── apps 
|     ├── Dashboard.py
|     ├── News.py
|     |__ Predictions.py 
├── assets
|     ├── favicon.ico
|     ├── css files and images
├── app.py
├── requirements.txt
├── index.py
├── Model.py
├── states_india.geojson (To plot the choropleth map)
|__ Procfile

```

## Setup Instructions:
The Code is written in Python 3.9. If you don't have Python installed you can find it [here](https://www.python.org/downloads/). 
```bash
git clone https://github.com/kadatatlukishore/Covid-19-Tracker-India.git
cd Covid-19-Tracker-India
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python3 index.py
```


## Technologies Used:
[<img target="_blank" src="https://ih1.redbubble.net/image.411682602.8572/st,small,845x845-pad,1000x1000,f8f8f8.u2.jpg" width=50>](https://www.python.org) [<img target="_blank" src="https://www.pngkit.com/png/detail/861-8618685_numfocus-plotly-dash-logo.png" width=50>](https://dash.plotly.com/) [<img target="_blank" src="https://pbs.twimg.com/profile_images/1187765724451868673/uVw1PWA7.png" width=50>](https://pandas.pydata.org/)[<img target="_blank" src="https://images.prismic.io/plotly-marketing-website/bd1f702a-b623-48ab-a459-3ee92a7499b4_logo-plotly.svg?auto=compress,format" width=80>](https://plotly.com/) [<img target="_blank" src="https://miro.medium.com/max/3600/1*fIjRtO5P8zc3pjs0E5hYkw.png" width=100>](https://www.heroku.com/)

-  If you find any problems in the site, kindly [Reach Me](https://www.linkedin.com/in/kishorekadatatlu/)
