using Microsoft.AspNetCore.Components;
using RpiHomeHub.BlazorWeb.Lights.Services;

namespace RpiHomeHub.BlazorWeb.Lights.Components
{
    public partial class LightControlsComponent<TLightModel> where TLightModel : class, ILightModel, new()
    {
        [Parameter]
        public LightServiceBase<TLightModel> Service { get; set; }

        [Parameter]
        public TLightModel Light { get; set; }
    }
}
