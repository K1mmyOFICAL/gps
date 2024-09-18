from kivy_garden.mapview import MapView, MapMarker, MapLayer
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from plyer import gps
import requests

class MapViewApp(App):
    def build(self):
        self.mapview = MapView(zoom=11, lat=50.6394, lon=3.057)

        layout = BoxLayout(orientation='vertical')
        btn_find_location = Button(text='Найти мою локацию', size_hint=(1, 0.1))
        btn_find_location.bind(on_release=self.start_gps)

        btn_find_route = Button(text='Построить маршрут', size_hint=(1, 0.1))
        btn_find_route.bind(on_release=self.find_route)

        layout.add_widget(btn_find_location)
        layout.add_widget(btn_find_route)
        layout.add_widget(self.mapview)

        return layout

    def start_gps(self, instance):
        try:
            gps.start(period=1, timeout=20)
            gps.bind(on_location=self.on_location)
        except NotImplementedError:
            print("GPS is not implemented for this platform.")

    def on_location(self, **kwargs):
        # Получение данных о местоположении
        lat = kwargs['lat']
        lon = kwargs['lon']
        print(f"Current Location: {lat}, {lon}")

        # Обновление карты с текущими координатами
        self.mapview.center_on(lat, lon)

    def find_route(self, instance):
        # Пример фиксированных координат для маршрута
        start_lat, start_lon = 50.6394, 3.057  # Текущая локация (например, моя локация)
        end_lat, end_lon = 50.6400, 3.0590  # Конечная точка маршрута

        # Удаление предыдущих маршрутов
        self.mapview.clear_widgets()

        # Добавляем маркеры для начала и конца маршрута
        start_marker = MapMarker(lat=start_lat, lon=start_lon)
        end_marker = MapMarker(lat=end_lat, lon=end_lon)
        self.mapview.add_widget(start_marker)
        self.mapview.add_widget(end_marker)

        # Пример логики для рисования линии (маршрута) между точками
        route_line = MapLayer(points=[start_lon, start_lat, end_lon, end_lat])
        self.mapview.add_widget(route_line)

if __name__ == '__main__':
    MapViewApp().run()