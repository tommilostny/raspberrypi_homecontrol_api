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

        private async Task Toggle() => Light = await LightService.ToggleAsync();

        private async Task TurnOn() => Light = await LightService.TurnOnAsync();

        private async Task TurnOff() => Light = await LightService.TurnOffAsync();
    }
}
