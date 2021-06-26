using Newtonsoft.Json;

namespace RpiHomeHub.BlazorWeb.Models
{
    public class YeelightBulbModel
    {
        public string Power { get; set; }

        [JsonProperty("bright")]
        public int Brightness { get; set; }

        [JsonProperty("ct")]
        public int Temperature { get; set; }

        public int RGB { get; set; }

        [JsonIgnore]
        public ColorRGB Color { get; set; }

        public int Hue { get; set; }

        [JsonProperty("sat")]
        public int Saturation { get; set; }
    }
}
