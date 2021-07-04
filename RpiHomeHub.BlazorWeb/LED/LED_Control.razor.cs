using Microsoft.AspNetCore.Components;
using RpiHomeHub.BlazorWeb.Colors;
using System;
using System.Net.Http;
using System.Threading.Tasks;

namespace RpiHomeHub.BlazorWeb.LED
{
    public partial class LED_Control : ComponentBase
    {
        [Inject]
        public HttpClient HttpClient { get; set; }

        [Parameter]
        public LED_Model Led { get; set; }

        private ColorRGB MappedColor { get; set; } = null;

        private async Task LED_Toggle() => await Led.ToggleAsync(HttpClient);

        private async Task LED_Blink() => await Led.BlinkAsync(HttpClient);

        private void IntervalInput_ChangeEvent(ChangeEventArgs e)
        {
            var inputValue = Convert.ToSingle(e.Value);
            Led.BlinkInterval = inputValue > 0F ? inputValue : 1F;
        }

        private string LedStatusAsString() => Led.IsActive ? "on" : "off";

        private string LedStatusImage() => $"led{Led.Number}{LedStatusAsString()}.jpg";

        protected override async Task OnInitializedAsync()
        {
            if (Led.IsRGB)
            {
                MappedColor = new ColorRGB
                {
                    Red = (int)(Led.Color[0] * 255F),
                    Green = (int)(Led.Color[1] * 255F),
                    Blue = (int)(Led.Color[2] * 255F),
                };
            }
            await base.OnInitializedAsync();
        }
    }
}
