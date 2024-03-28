# pip3 install pandas folium dash

cd /home/userver/DataEngProj/ISS_e2e_data_engineering_project/python_dash/Containerized

docker build -t dashboard-app .

docker run -d --name dashboard-app --network ISS_proj -p 8050:8050 dashboard-app

