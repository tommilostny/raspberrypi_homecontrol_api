using Microsoft.AspNetCore.Components;
using RpiHomeHub.BlazorWeb.Lights.Models;
using RpiHomeHub.BlazorWeb.Lights.Services;
using System.Threading.Tasks;

namespace RpiHomeHub.BlazorWeb.Lights.Components
{
    public partial class YeelightExtendedControls : ComponentBase
    {
        [Parameter]
        public YeelightModel Yeelight { get; set; }

        [Inject]
        public YeelightService YeelightService { get; set; }

        private async Task SetTemperature()
        {
            await YeelightService.SetTemperatureAsync(Yeelight.Temperature, Yeelight);
        }

        private async Task SetHS()
        {
            await YeelightService.SetHueSaturationAsync(Yeelight.Hue, Yeelight.Saturation, Yeelight);
        }
    }
}
