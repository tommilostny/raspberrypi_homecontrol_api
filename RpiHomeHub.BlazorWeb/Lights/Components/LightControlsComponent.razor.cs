using Microsoft.AspNetCore.Components;
using RpiHomeHub.BlazorWeb.Lights.Services;
using System.Threading.Tasks;

namespace RpiHomeHub.BlazorWeb.Lights.Components
{
    public partial class LightControlsComponent<TLightModel> where TLightModel : class, ILightModel, new()
    {
        [Parameter]
        public LightServiceBase<TLightModel> LightService { get; set; }

        [Parameter]
        public TLightModel Light { get; set; }

        private async Task Toggle() => await LightService.ToggleAsync(Light);

        private async Task TurnOn() => await LightService.TurnOnAsync(Light);

        private async Task TurnOff() => await LightService.TurnOffAsync(Light);

        private async Task Refresh()
        {
            var result = await LightService.GetStatusAsync();
            Light.Power = result.Power;
            Light.Brightness = result.Brightness;
            Light.Color.Red = result.Color.Red;
            Light.Color.Green = result.Color.Green;
            Light.Color.Blue = result.Color.Blue;
        }

        private async Task SetBrightness() => await LightService.SetBrightnessAsync(Light.Brightness, Light);
    }
}
