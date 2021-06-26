using Newtonsoft.Json;
using System.Collections.Generic;
using System.Net.Http;
using System.Threading.Tasks;

namespace RpiHomeHub.BlazorWeb.Models
{
    public class LED_Model
    {
        public List<int> Pins { get; set; }

        public bool IsActive { get; set; }

        public int Number { get; set; }

        public bool IsRGB { get; set; }

        public List<float> Color { get; set; }

        public string Name { get; set; }

        public bool Enabled { get; set; }

        [JsonIgnore]
        public float BlinkInterval { get; set; } = 1F;

        public async Task ToggleAsync(HttpClient httpClient)
            => await httpClient.GetAsync($"led/{Number}/{((IsActive = !IsActive) ? "on" : "off")}");

        public async Task BlinkAsync(HttpClient httpClient)
        {
            await httpClient.GetAsync($"led/{Number}/blink/{string.Format("{0:N2}", BlinkInterval)}");
            IsActive = true;
        }
    }
}
