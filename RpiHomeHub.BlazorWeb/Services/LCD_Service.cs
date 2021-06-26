using System.Net.Http;
using System.Threading.Tasks;

namespace RpiHomeHub.BlazorWeb.Services
{
    public class LCD_Service
    {
        public int LineWidth { get; set; }

        public int LinesCount { get; set; }

        private string _message = string.Empty;
        public string Message
        {
            get => _message;
            set => _message = value.Length <= LcdCapacity() ? value : value.Substring(0, LcdCapacity());
        }

        private readonly HttpClient _httpClient;

        public LCD_Service(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task SendMessageToLcd()
        {
            var lines = new string[LinesCount];
            for (int line = 0; line < LinesCount; line++)
            {
                lines[line] = string.Empty;
                for (int i = 0; i < LineWidth; i++)
                {
                    int index = i + line * LineWidth;
                    lines[line] += index < Message.Length ? Message[index] : ' ';
                }
                await _httpClient.GetAsync($"lcd_message/{lines[line]}/{line + 1}");
            }
        }

        public async Task LcdBacklightToggle() => await _httpClient.GetAsync("heater_lcd/2");

        public int LcdCapacity() => LineWidth * LinesCount;
    }
}
